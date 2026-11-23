package com.rit.cloudcart.controller;

import com.rit.cloudcart.model.Order;
import com.rit.cloudcart.model.Product;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;

@RestController
@RequestMapping("/api/orders")
public class OrderController {

    private final List<Order> orders = new CopyOnWriteArrayList<>();

    @GetMapping
    public List<Order> getAllOrders() {
        return orders;
    }

    @PostMapping
    public ResponseEntity<?> placeOrder(@RequestBody Map<String, Object> payload) {
        Long productId = payload.get("productId") != null ? Long.valueOf(payload.get("productId").toString()) : null;
        Integer quantity = payload.get("quantity") != null ? Integer.valueOf(payload.get("quantity").toString()) : 1;
        String email = payload.get("customerEmail") != null ? payload.get("customerEmail").toString().trim() : "";

        if (productId == null || !ProductController.CATALOG.containsKey(productId)) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(Map.of("status", 404, "error", "Not Found", "message", "Product ID " + productId + " does not exist"));
        }

        if (quantity == null || quantity <= 0 || email.isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(Map.of("status", 400, "error", "Bad Request", "message", "Quantity must be > 0 and customer email is required"));
        }

        Product product = ProductController.CATALOG.get(productId);
        synchronized (product) {
            if (product.getStock() < quantity) {
                return ResponseEntity.status(HttpStatus.CONFLICT)
                        .body(Map.of("status", 409, "error", "Conflict", "message", "Product " + productId + " is out of stock or insufficient inventory"));
            }
            product.setStock(product.getStock() - quantity);
        }

        String orderId = "ORD-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
        double total = product.getPrice() * quantity;
        Order order = new Order(orderId, productId, quantity, email, total, LocalDateTime.now());
        orders.add(order);

        return ResponseEntity.status(HttpStatus.CREATED).body(order);
    }
}
