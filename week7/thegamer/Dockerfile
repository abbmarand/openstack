FROM nginx

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install wget unzip -y
RUN cd
RUN wget -q -O /thegamer.zip https://canvas.mdu.se/courses/13197/files/1810776/download
RUN wget -q -O /techblog.zip https://canvas.mdu.se/courses/13197/files/1810775/download
RUN mkdir thegamer techblog
RUN mv thegamer.zip thegamer
RUN unzip thegamer/thegamer.zip -d thegamer
RUN mv techblog.zip techblog
RUN unzip techblog/techblog.zip -d techblog
RUN rm -rf techblog/*.zip thegamer/*.zip

COPY default.conf /etc/nginx/conf.d/

COPY --chown=root:root start.bash .
RUN chmod +x start.bash
CMD "./start.bash"