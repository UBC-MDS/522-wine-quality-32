FROM quay.io/jupyter/minimal-notebook:afe30f0c9ad8

# Switch to root user for installing system dependencies
USER root

# Install make, LaTeX packages, and clean up
RUN apt-get update && apt-get install -y make texlive-latex-extra lmodern && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the Conda lock file into the container
COPY conda-linux-64.lock /tmp/conda-linux-64.lock

# Switch to non-root user temporarily for conda environment updates
USER jovyan

# Update Conda environment using mamba
RUN mamba update --quiet --file /tmp/conda-linux-64.lock && \
    mamba clean --all -y -f

# Switch back to root to install pip dependencies
USER root

# Extract and install pip dependencies from the lock file
RUN grep '^# pip ' /tmp/conda-linux-64.lock | cut -d' ' -f3 | xargs pip install --no-cache-dir

# Fix permissions to ensure compatibility with non-root user
RUN fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Switch back to non-root user
USER ${NB_USER}

# Set the working directory
WORKDIR /home/jovyan