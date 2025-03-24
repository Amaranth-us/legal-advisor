# Stage 1: Set up the common environment
FROM python:3.13-slim AS env

# Define build arguments
ARG FASTAPI_CODE_PATH="/code"
ARG FASTAPI_VENV_NAME="../.venv"
ARG USERNAME="appuser"
ARG USER_UID="1001"
ARG USER_GID="1001"

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Add a non-root user with permissions to a working directory
RUN groupadd --gid ${USER_GID} -r ${USERNAME} && \
    useradd --gid ${USER_GID} --uid ${USER_UID} -l -m -r ${USERNAME} && \
    mkdir -p ${FASTAPI_CODE_PATH} && \
    chown -R ${USERNAME}:${USER_GID} ${FASTAPI_CODE_PATH}

# Stage 2: Install all the packages
FROM env AS build

WORKDIR ${FASTAPI_CODE_PATH}

# Copy requirements first, install dependencies
COPY requirements.txt ${FASTAPI_CODE_PATH}
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 && \
    apt-get upgrade -y && \
    python -m venv ${FASTAPI_VENV_NAME} && \
    . ${FASTAPI_VENV_NAME}/bin/activate && \
    python -m pip install --upgrade pip setuptools && \
    pip install -r requirements.txt && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Stage 3: Set up the runtime environment and copy files
FROM env AS runtime

USER ${USERNAME}

# Setup the PATH to use the virtual environment
ENV PATH="${FASTAPI_CODE_PATH}/${FASTAPI_VENV_NAME}/bin:$PATH"

# Copy the virtual environment from the build stage
COPY --from=build ${FASTAPI_CODE_PATH}/${FASTAPI_VENV_NAME} ${FASTAPI_VENV_NAME}

# Copy all source code (including .env and init.sql)
COPY . ./

EXPOSE 8081

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
