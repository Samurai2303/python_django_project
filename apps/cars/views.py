from rest_framework.views import APIView, Response, status

from .models import CarModel
from .serializers import CarSerializer, CarSerializerShort


class CarsView(APIView):
    def get(self, *args, **kwargs):
        cars = CarModel.objects.all()
        serializer = CarSerializerShort(instance=cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = CarSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CarByIdView(APIView):
    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        exists = CarModel.objects.filter(pk=pk).exists()
        if not exists:
            return Response('Not found', status=status.HTTP_404_NOT_FOUND)
        car = CarModel.objects.get(pk=pk)
        serializer = CarSerializer(instance=car)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, *args, **kwargs):
        pk = kwargs.get('pk')
        data = self.request.data
        exists = CarModel.objects.filter(pk=pk).exists()
        if not exists:
            return Response('Car not found', status=status.HTTP_404_NOT_FOUND)
        car = CarModel.objects.get(pk=pk)
        serializer = CarSerializer(car, data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        pk = kwargs.get('pk')
        data = self.request.data
        exists = CarModel.objects.filter(pk=pk).exists()
        if not exists:
            return Response('Car not found', status=status.HTTP_404_NOT_FOUND)
        car = CarModel.objects.get(pk=pk)
        serializer = CarSerializer(car, data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        pk = kwargs.get('pk')
        exists = CarModel.objects.filter(pk=pk).exists()
        if not exists:
            return Response('Car not found', status=status.HTTP_404_NOT_FOUND)
        car = CarModel.objects.get(pk=pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
