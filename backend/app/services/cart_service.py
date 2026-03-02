from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.product_repository import ProductRepository
from app.schemas.cart import CartItemCreate, CartResponse, CartItemUpdate, CartItem

class CartService:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)

    def add_to_cart(self, cart_data: Dict[int, int], item: CartItemCreate) -> Dict[int, int]:
        product = self.product_repository.get_by_id(item.product_id)
        if not product:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Product with ID {item.product_id} not found"
            )
        
        if item.product_id in cart_data:
            cart_data[item.product_id] += item.quantity
        else:
            cart_data[item.product_id] = item.quantity
        return cart_data


    def update_cart_item(self, cart_data: Dict[int, int], item: CartItemCreate) -> Dict[int, int]:
        if item.product_id not in cart_data:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Product with ID {item.product_id} not found in cart"
            )
        
        if item.quantity <= 0:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Quantity must be greater than 0"
            )
        
        cart_data[item.product_id] = item.quantity
        return cart_data

    def remove_from_cart(self, cart_data: Dict[int, int], product_id: int) -> Dict[int, int]:
        if product_id not in cart_data:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Product with ID {product_id} not found in cart"
            )
        
        del cart_data[product_id]
        return cart_data

    def get_cart_details(self, cart_data: Dict[int, int]) -> CartResponse:
        if not cart_data:
            return CartResponse(
                items = [],
                total = 0,
                items_count = 0
            )
        
        products = self.product_repository.get_multiple_by_ids(list(cart_data.keys()))
        if not products:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Products not found"
            )

        cart_items = []
        total = 0.0
        items_count = 0

        for product in products:
            if product.id in cart_data:
                quantity = cart_data[product.id]
                subtotal = product.price * quantity
                total += subtotal
                items_count += quantity
                cart_items.append(
                    CartItem(
                        product_id=product.id,
                        name=product.name,
                        price=product.price,
                        quantity=quantity,
                        subtotal=subtotal,
                        image_url=product.image_url
                    )
                )

        return CartResponse(
            items = cart_items,
            total = total,
            items_count = items_count
        )
