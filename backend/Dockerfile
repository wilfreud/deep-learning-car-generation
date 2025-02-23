# Use an official TensorFlow CPU image as the base
FROM tensorflow/tensorflow:latest

# Set the working directory
WORKDIR /app

# Create a user named 'commodore'
RUN useradd -m commodore && \
    chown -R commodore:commodore /app

# Switch to the 'commodore' user
USER commodore

# Copy your code into the container
COPY --chown=commodore:commodore . .

# Install FastAPI, Uvicorn, and other dependencies
RUN pip install fastapi uvicorn diffusers pydantic transformers torch

# Expose port 8000
EXPOSE 8000

# Ensure permissions are set correctly
RUN chmod -R 755 /app

# Command to run the FastAPI app (using ENTRYPOINT instead of CMD)
ENTRYPOINT ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
