FROM php:8.2-cli-alpine

WORKDIR /var/www/html

# Dependencias del sistema
RUN apk add --no-cache \
    git \
    curl \
    libpng-dev \
    libxml2-dev \
    zip \
    unzip \
    postgresql-dev \
    oniguruma-dev \
    nodejs \
    npm

# Extensiones PHP
# $PHPIZE_DEPS incluye autoconf y herramientas de build requeridas por pecl
RUN apk add --no-cache --virtual .build-deps $PHPIZE_DEPS \
    && docker-php-ext-install pdo pdo_pgsql mbstring xml bcmath opcache gd \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && apk del .build-deps

# Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Instalar dependencias PHP
COPY composer.json composer.lock ./
RUN composer install --no-dev --optimize-autoloader --no-scripts --no-interaction

# Instalar dependencias Node y compilar frontend
COPY package.json package-lock.json ./
RUN npm ci

# Copiar el resto de la aplicacion
COPY . .

# Compilar assets de Vue.js/Vite
RUN npm run build

# Ejecutar scripts post-instalacion de Composer
RUN php artisan package:discover --ansi

# Crear directorios y permisos de storage
RUN mkdir -p storage/logs \
    storage/framework/cache \
    storage/framework/sessions \
    storage/framework/views \
    bootstrap/cache \
    && chmod -R 775 storage bootstrap/cache

EXPOSE ${PORT:-8000}

CMD ["sh", "-c", "php artisan migrate --force && php artisan storage:link && php artisan config:cache && php artisan route:cache && php artisan serve --host=0.0.0.0 --port=${PORT:-8000}"]
