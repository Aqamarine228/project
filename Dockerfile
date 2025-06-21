# Signal Visualization Application Dockerfile
# Multi-stage build to reduce memory usage
FROM python:3.9-slim as builder

# Set environment variables for build stage
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --user --no-warn-script-location \
    numpy==1.21.6 \
    && pip install --user --no-warn-script-location \
    PyQt5==5.15.7 \
    && pip install --user --no-warn-script-location \
    vispy \
    && pip install --user --no-warn-script-location \
    matplotlib

# Production stage
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV PATH=/root/.local/bin:$PATH

# Install system dependencies for PyQt5 and GUI applications
RUN apt-get update && apt-get install -y \
    qtbase5-dev \
    qtchooser \
    qt5-qmake \
    qtbase5-dev-tools \
    libqt5gui5 \
    libqt5core5a \
    libqt5widgets5 \
    libqt5dbus5 \
    libqt5network5 \
    libqt5svg5-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libice6 \
    libxrender1 \
    libfontconfig1 \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libasound2 \
    x11-apps \
    python3-pyqt5 \
    python3-pyqt5.qtsvg \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Create application directory
WORKDIR /app

# Copy application code
COPY . .

# Create runtime directory
RUN mkdir -p /tmp/runtime-root

# Set permissions
RUN chmod -R 755 /app
RUN chmod +x tcp_test_server.py

# Expose default TCP port for test server
EXPOSE 12345

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
if [ "$1" = "server" ]; then\n\
    echo "Starting TCP Test Server..."\n\
    exec python tcp_test_server.py --host 0.0.0.0 --port 12345 "${@:2}"\n\
elif [ "$1" = "app" ]; then\n\
    echo "Starting Signal Visualization Application..."\n\
    exec python main.py\n\
else\n\
    echo "Usage: docker run [OPTIONS] IMAGE [server|app] [ARGS...]"\n\
    echo ""\n\
    echo "Commands:"\n\
    echo "  server    Start TCP test server"\n\
    echo "  app       Start signal visualization application"\n\
    echo ""\n\
    echo "Examples:"\n\
    echo "  docker run -p 12345:12345 image server"\n\
    echo "  docker run -e DISPLAY=\$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix image app"\n\
    exit 1\n\
fi' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["server"]