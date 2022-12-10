FROM quay.io/keycloak/keycloak:20.0.1 as builder
#jar file
COPY ojdbc11.jar /opt/keycloak/lib/lib/main/
RUN java -jar /opt/keycloak/lib/lib/main/ojdbc11.jar
#metrics-spi for monitoring
COPY keycloak-metrics-spi*.jar /opt/keycloak/providers/
RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:20.0.1
#metrics-spi for monitoring
COPY keycloak-metrics-spi*.jar /opt/keycloak/providers/
#oracle conf
RUN bash -c "/opt/keycloak/bin/kc.sh build --db=oracle"
COPY --from=builder /opt/keycloak/lib/quarkus/ /opt/keycloak/lib/quarkus/
WORKDIR /opt/keycloak
RUN chown keycloak:keycloak data/
RUN keytool -genkeypair -storepass password -storetype PKCS12 -keyalg RSA -keysize 2048 -dname "CN=server" -alias server -ext "SAN:c=DNS:localhost,IP:127.0.0.1" -keystore conf/server.keystore
ENTRYPOINT /opt/keycloak/bin/kc.sh start
