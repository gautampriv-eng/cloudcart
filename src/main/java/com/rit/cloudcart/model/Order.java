package com.rit.cloudcart.model;

import java.time.LocalDateTime;

public class Order {
    private String orderId;
    private Long productId;
    private int quantity;
    private String customerEmail;
    private double totalAmount;
    private LocalDateTime orderTime;

    public Order() {}

    public Order(String orderId, Long productId, int quantity, String customerEmail, double totalAmount, LocalDateTime orderTime) {
        this.orderId = orderId;
        this.productId = productId;
        this.quantity = quantity;
        this.customerEmail = customerEmail;
        this.totalAmount = totalAmount;
        this.orderTime = orderTime;
    }

    public String getOrderId() { return orderId; }
    public void setOrderId(String orderId) { this.orderId = orderId; }

    public Long getProductId() { return productId; }
    public void setProductId(Long productId) { this.productId = productId; }

    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; }

    public String getCustomerEmail() { return customerEmail; }
    public void setCustomerEmail(String customerEmail) { this.customerEmail = customerEmail; }

    public double getTotalAmount() { return totalAmount; }
    public void setTotalAmount(double totalAmount) { this.totalAmount = totalAmount; }

    public LocalDateTime getOrderTime() { return orderTime; }
    public void setOrderTime(LocalDateTime orderTime) { this.orderTime = orderTime; }
}
