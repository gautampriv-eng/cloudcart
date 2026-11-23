# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn -B dependency:go-offline
COPY src ./src
RUN mvn -B clean package -DskipTests

# Stage 2: Minimal runtime stage
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/target/cloudcart.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
