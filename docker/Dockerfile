# FROM python:3.9
#
# # Set the working directory
# WORKDIR /usr/src/app
#
# USER root
#
# # Copy the requirements file
# COPY requirements.txt ./requirements.txt
#
#
# # Install the dependencies
# RUN python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
# RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
#
# # Copy the rest of the source code
# COPY main.py ./main.py
# COPY sea_surface_temp_raster.tiff ./sea_surface_temp_raster.tiff
# COPY shandong.geojson ./shandong.geojson
#
#
# CMD ["python", "main.py"]



FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y libpq-dev
RUN apt-get install -y gdal-bin
RUN apt-get upgrade -y gdal-bin
RUN apt-get install -y libgdal-dev
RUN apt-get install -y python3-pip python3-dev

RUN cd /usr/local/bin \
  && ln -s /usr/bin/python3 python

RUN mkdir -p /home/pieuser
WORKDIR /home/pieuser
COPY requirements.txt requirements.txt
COPY main.py ./main.py
COPY sea_surface_temp_raster.tiff ./sea_surface_temp_raster.tiff
COPY shandong.geojson ./shandong.geojson
RUN pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ENTRYPOINT ["python3", "main.py"]







