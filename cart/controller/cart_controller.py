from rest_framework.response import Response
from rest_framework.views import APIView

from cart.dto.cart.cart_input_dto import CartInputDto
from cart.dto.cart.cart_output_dto import CartOutputDto
from cart.models import Cart, Product, ProductRefCart


class CartController(APIView):

    def get(self, request):
        # get user_id from jwt token
        user_id = 1
        cart = Cart.objects.get(user_id=user_id)
        return Response(CartOutputDto(cart).data)

    def put(self, request):
        user_id = 1
        cart_input = CartInputDto(data=request.data)
        if cart_input.is_valid():
            cart = Cart.objects.get(user_id=user_id)
            product_id = cart_input.validated_data.get('product_id')
            type = cart_input.validated_data.get('type')
            quantity = cart_input.validated_data.get('quantity')
            product = Product.objects.filter(type=type, product_id=product_id)
            if not product.exists():
                product = Product.objects.create(type=type, product_id=product_id)
            else:
                product = product.first()
            product_ref_cart = ProductRefCart.objects.filter(cart_id=cart.id, product_id=product.id)
            if product_ref_cart.exists():
                product_ref_cart = product_ref_cart.first()
                product_ref_cart.quantity += quantity
                if product_ref_cart.quantity <= 0:
                    product_ref_cart.delete()
                else:
                    product_ref_cart.save()
            else:
                if quantity > 0:
                    ProductRefCart.objects.create(cart_id=cart, product_id=product, quantity=quantity)
            return Response(CartOutputDto(Cart.objects.get(user_id=user_id)).data)
