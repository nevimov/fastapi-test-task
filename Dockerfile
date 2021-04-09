# Useful links:
# https://docs.docker.com/engine/reference/builder/
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

FROM python:3.9.3-buster

# This Dockerfile adds a non-root user with sudo access. However, for Linux,
# this user's GID/UID must match your local user UID/GID to avoid permission
# issues with bind mounts. Update USER_UID / USER_GID if yours is not 1000.
# See https://aka.ms/vscode-remote/containers/non-root-user for details.
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV PROJECT_ROOT_DIR=/project
ENV PYTHONPATH=$PROJECT_ROOT_DIR

# Fix "Warning: Unable to set locale. Expect encoding problems."
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    #
    # INSTALL DEBIAN PACKAGES
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    && apt-get install --assume-yes \
        #
        # Install packages important for CLI installs
        procps \
        sudo \
        #
        # python3-dev is required to build Psycopg from source
        python3-dev \
        python3-pip \
    #
    # Remove APT cache and package lists to reduce disk space occupied by the container
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    #
    # INSTALL NODE.JS AND NPM
    && curl -fsSL https://deb.nodesource.com/setup_15.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    #
    # INSTALL DART SASS'S STAND-ALONE EXECUTABLE (faster than the JS version)
    && export SASS_VERSION=1.32.8 \
    && export SASS_ARCHIVE=dart-sass-${SASS_VERSION}-linux-x64.tar.gz \
    && cd /usr/local/bin \
    && wget --progress=dot --quiet \
    "https://github.com/sass/dart-sass/releases/download/$SASS_VERSION/$SASS_ARCHIVE" \
    # Extract the archive without the root folder
    && tar -xf  "$SASS_ARCHIVE" --strip-components=1 \
    && rm "$SASS_ARCHIVE" \
    #
    # CREATE A NON-ROOT USER
    && groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # [Optional] Add sudo support for the non-root user
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    #
    # CREATE PROJECT DIRECTORIES
    && mkdir -p "$PROJECT_ROOT_DIR" \
    && chown $USER_UID:$USER_GID "$PROJECT_ROOT_DIR"

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=

WORKDIR $PROJECT_ROOT_DIR


# INSTALL PYTHON DEPENDENCIES
COPY requirements.txt requirements-dev.txt ./
RUN pip3 install --no-cache-dir --requirement requirements-dev.txt


# INSTALL NODE PACKAGES
USER $USER_UID:$USER_GID
COPY package*.json ./
RUN npm install && npm cache clean --force --loglevel=error


EXPOSE 8000
CMD ["sleep", "infinity"]
