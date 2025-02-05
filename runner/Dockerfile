FROM python:3.11

ARG USER_ID=1000
ARG GROUP_ID=1000
RUN echo "Used user id: ${USER_ID}\nUsed group id: ${GROUP_ID}"

# Update system
RUN apt update && apt upgrade -y && apt autoremove -y

# Upgrade python package manager
RUN pip install --upgrade pip

# Change working directory
WORKDIR /home/runner

# Copy folders and files – It's important to copy files before changing their ownership
COPY ./.git ./.git
COPY ./src ./src
COPY ./pyproject.toml ./pyproject.toml
COPY ./config ./config

# Change ID of runner user and group to ID from ENV
RUN if [ ${USER_ID:-1000} -ne 0 ] && [ ${GROUP_ID:-1000} -ne 0 ]; then \
  if getent passwd runner ; then echo "Delete user runner" && userdel -f runner;fi &&\
  if getent group runner ; then echo "Delete group runner" && groupdel runner;fi &&\
  echo "Add new group runner" && groupadd -g ${GROUP_ID} runner &&\
  echo "Add new user runner" && useradd -l -u ${USER_ID} -g runner runner &&\
  echo "Change ownership of workdir" && mkdir -p /var/www && chown --changes --no-dereference --recursive runner:runner /var/www &&\
  echo "Change ownership of homedir" && mkdir -p /home/runner && chown --changes --no-dereference --recursive runner:runner /home/runner \
  ;fi

# BEGIN Install supercronic to run regular jobs in the container

# Latest releases available at https://github.com/aptible/supercronic/releases
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.32/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=7da26ce6ab48d75e97f7204554afe7c80779d4e0

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

# Change ownership in home dir
RUN chown --changes --silent --no-dereference --recursive ${USER_ID}:${GROUP_ID} /home/runner/

# Change the user and group
USER ${USER_ID}:${GROUP_ID}

# Change working directory
WORKDIR /home/runner

# Create PDM environment
RUN pip install pdm && python -m pdm install

# Just test the crontab format
RUN set -eux; \
  /usr/local/bin/supercronic -test -debug /home/runner/config/default.crontab

# Run Supercronic when the container starts
CMD /usr/local/bin/supercronic /home/runner/config/default.crontab

# Uncomment this to keep the container running forever
#CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"

