FROM python:3

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y netcat

# Create an app user
RUN useradd --user-group --create-home --no-log-init --shell /bin/bash appuser

ENV APPUSER_HOME=/home/appuser
ENV APP_HOME=/home/appuser/webapp

# Create the staticfiles directory. This avoids permission errors.
RUN mkdir -p $APPUSER_HOME/static_cdn/static_root \
&& mkdir -p $APPUSER_HOME/static_cdn/media_root \
&& mkdir -p $APPUSER_HOME/static_cdn/protected_media \
&& mkdir -p $APP_HOME/static_webapp

WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . $APP_HOME

RUN chown -R appuser:appuser $APPUSER_HOME

USER appuser:appuser

ENTRYPOINT ["/home/appuser/webapp/entrypoint.sh"]
