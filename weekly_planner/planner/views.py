from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Activity

@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def activities(request):
    user = request.user

    if request.method == "POST":
        # Create a new activity
        data = request.data
        activity = Activity(
            name=data.get("name"),
            user=user,
        )
        activity.save()
        return Response({"message": "Activity added successfully."}, status=status.HTTP_201_CREATED)

    elif request.method == "GET":
        # List all activities for the user
        activities = Activity.objects.filter(user=user)
        return Response(
            [{"id": a.id, "name": a.name, "is_completed": a.is_completed, "deadline": a.deadline} for a in activities]
        )

    elif request.method == "PUT":
        # Update an activity
        data = request.data
        try:
            activity = Activity.objects.get(id=data.get("id"), user=user)
        except Activity.DoesNotExist:
            return Response({"error": "Activity not found."}, status=status.HTTP_404_NOT_FOUND)

        activity.name = data.get("name", activity.name)
        activity.is_completed = data.get("is_completed", activity.is_completed)
        activity.save()
        return Response({"message": "Activity updated successfully."})

    elif request.method == "DELETE":
        # Delete an activity
        data = request.data
        try:
            activity = Activity.objects.get(id=data.get("id"), user=user)
        except Activity.DoesNotExist:
            return Response({"error": "Activity not found."}, status=status.HTTP_404_NOT_FOUND)

        activity.delete()
        return Response({"message": "Activity deleted successfully."})
