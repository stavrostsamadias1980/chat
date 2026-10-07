# ==============================================================================
# STAGE 1: Build Angular Deep Chat Frontend
# ==============================================================================
FROM node:20-alpine AS frontend-builder
WORKDIR /app/ui

# Install dependencies
COPY UI/package*.json ./
RUN npm ci

# Copy Angular source and build
COPY UI/ ./
RUN npm run build -- --configuration production

# ==============================================================================
# STAGE 2: Build Pure Java 21 Spring Boot Backend
# ==============================================================================
FROM eclipse-temurin:21-jdk-alpine AS backend-builder
WORKDIR /app/backend

# Copy Gradle files
COPY BACKEND_JAVA/gradle/ ./gradle/
COPY BACKEND_JAVA/gradlew ./
COPY BACKEND_JAVA/build.gradle ./
COPY BACKEND_JAVA/settings.gradle ./
RUN chmod +x gradlew

# Copy Java source code
COPY BACKEND_JAVA/src/ ./src/

# Copy Angular build into Spring Boot static resources (so Spring Boot serves both UI & WebSockets!)
RUN mkdir -p src/main/resources/static
COPY --from=frontend-builder /app/ui/dist/anytime-chatbot-ui/browser/ src/main/resources/static/

# Build standalone bootJar
RUN ./gradlew bootJar --no-daemon -x test

# ==============================================================================
# STAGE 3: Production Runtime
# ==============================================================================
FROM eclipse-temurin:21-jre-alpine AS runner
WORKDIR /app

# Create non-root system user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy dataset files needed for in-memory RAG search
COPY anytime_rag_dataset/ /app/anytime_rag_dataset/

# Copy compiled executable JAR
COPY --from=backend-builder /app/backend/build/libs/anytime-chatbot-backend-3.0.0.jar /app/app.jar

USER appuser

EXPOSE 8088

ENV SPRING_PROFILES_ACTIVE=prod
ENV ANYTIME_DATASET_PATH=/app/anytime_rag_dataset/rag_ready_chunks
ENV JAVA_OPTS="-Xms256m -Xmx512m -XX:+UseG1GC"

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/app.jar"]
