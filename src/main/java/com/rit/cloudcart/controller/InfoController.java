package com.rit.cloudcart.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.LinkedHashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/info")
public class InfoController {

    @Value("${app.message:Welcome to CloudCart E-Commerce API}")
    private String message;

    @Value("${app.version:1.0.0}")
    private String version;

    @GetMapping
    public Map<String, Object> getInfo() {
        Map<String, Object> info = new LinkedHashMap<>();
        info.put("app", "CloudCart");
        info.put("version", version);
        info.put("message", message);
        String podName = System.getenv("HOSTNAME");
        info.put("pod", podName != null ? podName : "localhost");
        return info;
    }
}
