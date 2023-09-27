from rest_framework import generics

from community.models import Community
from community.serializers import CommunityListSerializer


class GetCommunities(generics.ListAPIView):
    serializer_class = CommunityListSerializer
    queryset = Community.objects.all()
