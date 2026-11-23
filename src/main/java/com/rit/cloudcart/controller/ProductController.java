package com.rit.cloudcart.controller;

import com.rit.cloudcart.model.Product;
import org.springframework.web.bind.annotation.*;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@RestController
@RequestMapping("/api/products")
public class ProductController {

    public static final Map<Long, Product> CATALOG = new ConcurrentHashMap<>();

    static {
        CATALOG.put(1L, new Product(1L, "Wireless Mechanical Keyboard", "Electronics", 79.99, 15));
        CATALOG.put(2L, new Product(2L, "Ergonomic Gaming Mouse", "Electronics", 49.99, 25));
        CATALOG.put(3L, new Product(3L, "Ultra-Wide Monitor 34-inch", "Electronics", 349.99, 1));
    }

    @GetMapping
    public List<Product> getAllProducts() {
        return new ArrayList<>(CATALOG.values());
    }

    @GetMapping("/{id}")
    public Product getProductById(@PathVariable Long id) {
        Product p = CATALOG.get(id);
        if (p == null) {
            throw new NoSuchElementException("Product not found");
        }
        return p;
    }
}
