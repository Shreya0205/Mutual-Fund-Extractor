from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from funds.models import MutualFundFamily, MutualFundScheme
from funds.serializers import MutualFundFamilySerializer, MutualFundSchemeSerializer
from funds.services import MutualFundService


class MutualFundFamilyViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MutualFundFamilySerializer
    queryset = MutualFundFamily.objects

    def list(self, request):
        """
        Get all registered fund families.
        """
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Register a new fund family and fetch its schemes.
        """
        mutual_fund_family = request.data.get("mutual_fund_family")

        if not mutual_fund_family:
            return Response({"error": "Mutual Fund Family is required"}, status=status.HTTP_400_BAD_REQUEST)

        if self.queryset.filter(mutual_fund_family=mutual_fund_family).exists():
            return Response({"error": "Mutual Fund Family is already registered"}, status=status.HTTP_400_BAD_REQUEST)

        result = MutualFundService.fetch_open_ended_schemes_for_family(mutual_fund_family)

        if result.get("success"):

            if len(result.get("data")) == 0 :
                return Response(
                    {"error": "No open ended scheme found for the family. Family not registered."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serialized = MutualFundFamilySerializer(data=request.data)
            serialized.is_valid(raise_exception=True)
            instance = serialized.save()
            MutualFundService.save_schemes_to_db(instance, result)

            return Response(
                {"message": "successfully saved"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": result.get("error", "An unknown error occurred.")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def schemes(self, request):
        """
        Fetch schemes based on fund_family parameter.
        """
        mutual_fund_family = request.query_params.get("mutual_fund_family")
        if not mutual_fund_family:
            return Response({"error": "Fund Family parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mutual_fund_family_obj = self.queryset.get(mutual_fund_family=mutual_fund_family)
        except MutualFundFamily.DoesNotExist:
            return Response({"error": "Mutual Fund family not registered."}, status=status.HTTP_404_NOT_FOUND)

        schemes = MutualFundScheme.objects.filter(mutual_fund_family=mutual_fund_family_obj.id)
        serializer = MutualFundSchemeSerializer(schemes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)