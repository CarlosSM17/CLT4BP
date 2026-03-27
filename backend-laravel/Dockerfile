FROM php:8.2-apache

WORKDIR /var/www/html

# Dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    libpng-dev \
    libxml2-dev \
    zip \
    unzip \
    libpq-dev \
    libonig-dev \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Extensiones PHP
RUN docker-php-ext-install pdo pdo_pgsql mbstring xml bcmath opcache gd \
    && pecl install redis \
    && docker-php-ext-enable redis

# Habilitar mod_rewrite para Laravel
RUN a2enmod rewrite

# Apache config: document root en /public, puerto 8080
COPY docker/apache.conf /etc/apache2/sites-available/000-default.conf

# Cambiar puerto de Apache a 8080 en tiempo de build
RUN sed -i 's/^Listen 80$/Listen 8080/' /etc/apache2/ports.conf

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
    && chmod -R 775 storage bootstrap/cache \
    && chown -R www-data:www-data storage bootstrap/cache

EXPOSE 8080

CMD ["bash", "-c", "php artisan migrate --force && (php artisan storage:link || true) && php artisan config:cache && php artisan route:cache && apache2-foreground"]
