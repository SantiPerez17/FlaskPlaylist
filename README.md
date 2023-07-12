# Playlist

Playlist es una aplicación web desarrollada en Flask que te permite crear y gestionar tus propias listas de reproducción de música. Con Playlist, puedes agregar canciones, organizarlas en listas personalizadas y disfrutar de tu música favorita en cualquier momento.

## Características principales

- Registro de usuarios: Crea una cuenta y accede a todas las funciones de Playlist.
- Autenticación segura: Protege tus datos con un sistema de autenticación basado en tokens JWT.
- Creación de listas de reproducción: Crea listas personalizadas con tus canciones favoritas.
- Administración de canciones: Agrega y elimina canciones de tus listas de reproducción.
- Exploración de canciones: Descubre nuevas canciones y géneros populares.
- Edición de perfil: Actualiza tu información de usuario, incluyendo nombre de usuario y contraseña.

## Instalación

1. Clona el repositorio de Playlist.
2. Crea y activa un entorno virtual.
3. Instala las dependencias del proyecto: `pip install -r requirements.txt`.
4. Ejecuta la aplicación: `python run.py`.

## Tabla de contenidos

- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Endpoints](#endpoints)

## Requisitos previos

- Python
- Flask
- SQLAlchemy

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/SantiPerez17/FlaskPlaylist.git
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno (si es necesario).

## Uso

1. Inicia la aplicación:

```bash
python run.py
```

2. Accede a la aplicación en tu navegador:

```
http://localhost:5000
```

3. Interactúa con la aplicación según su funcionalidad.

## Endpoints

Aquí se describen los endpoints disponibles en el proyecto:

Por supuesto, aquí tienes la documentación para los endpoints proporcionados:

## Endpoints de Users

### Agregar un nuevo usuario
```
POST /users/
```
Este endpoint permite agregar un nuevo usuario.

#### Parámetros de entrada
- `email`: Dirección de correo electrónico del usuario.
- `username`: Nombre de usuario del usuario.
- `password`: Contraseña del usuario.

#### Respuestas
- `200 OK`: El usuario se ha creado correctamente.
- `400 Bad Request`: Los datos de la solicitud son inválidos o faltan campos requeridos.
- `500 Internal Server Error`: Se produjo un error al guardar la información del usuario.

### Iniciar sesión de usuario
```
POST /users/login
```
Este endpoint permite a un usuario iniciar sesión y obtener un token de autenticación.

#### Parámetros de entrada
- `email`: Dirección de correo electrónico del usuario.
- `password`: Contraseña del usuario.

#### Respuestas
- `200 OK`: El inicio de sesión fue exitoso y se devuelve un token de autenticación.
- `401 Unauthorized`: Las credenciales de inicio de sesión son inválidas.
- `500 Internal Server Error`: Se produjo un error al verificar las credenciales.

### Obtener todos los usuarios
```
GET /users/
```
Este endpoint devuelve una lista de todos los usuarios registrados.

#### Respuesta
- `200 OK`: La lista de usuarios se ha obtenido correctamente.
- `500 Internal Server Error`: Se produjo un error al obtener los usuarios.

### Obtener información de un usuario por ID
```
GET /users/{id}
```
Este endpoint permite obtener información de un usuario específico según su ID.

#### Parámetros de entrada
- `id`: ID del usuario.

#### Respuestas
- `200 OK`: El usuario se ha encontrado y se devuelve su información.
- `404 Not Found`: El usuario no se encontró en la base de datos.

### Eliminar un usuario
```
DELETE /users/{id}
```
Este endpoint permite eliminar un usuario según su ID.

#### Parámetros de entrada
- `id`: ID del usuario a eliminar.

#### Respuestas
- `200 OK`: El usuario se ha eliminado correctamente.
- `404 Not Found`: El usuario no se encontró en la base de datos.
- `500 Internal Server Error`: Se produjo un error al eliminar el usuario.

### Actualizar información de un usuario
```
PUT /users/{id}
```
Este endpoint permite actualizar la información de un usuario según su ID.

#### Parámetros de entrada
- `id`: ID del usuario a actualizar.
- `username` (opcional): Nuevo nombre de usuario del usuario.
- `email` (opcional): Nueva dirección de correo electrónico del usuario.

#### Respuestas
- `200 OK`: El usuario se ha actualizado correctamente.
- `400 Bad Request`: Los datos de la solicitud son inválidos.
- `404 Not Found`: El usuario no se encontró en la base de datos.
- `500 Internal

 Server Error`: Se produjo un error al actualizar el usuario.

### Cambiar la contraseña de un usuario
```
PUT /users/change_password
```
Este endpoint permite cambiar la contraseña de un usuario. Se requiere autenticación con un token válido.

#### Parámetros de entrada
- `current_password`: Contraseña actual del usuario.
- `new_password`: Nueva contraseña del usuario.

#### Respuestas
- `200 OK`: La contraseña se ha cambiado correctamente.
- `400 Bad Request`: Los datos de la solicitud son inválidos.
- `401 Unauthorized`: Se requiere autenticación para acceder al recurso.
- `500 Internal Server Error`: Se produjo un error al cambiar la contraseña.


## Endpoints de Songs

### Agregar una nueva canción
```
POST /songs/
```
Este endpoint permite agregar una nueva canción. Se requiere autenticación con un token válido.

#### Parámetros de entrada
- `name`: Nombre de la canción.
- `author`: Autor de la canción.
- `genre`: Género de la canción.

#### Respuestas
- `200 OK`: La canción se ha creado correctamente.
- `400 Bad Request`: Los datos de la solicitud son inválidos o faltan campos requeridos.
- `401 Unauthorized`: Se requiere autenticación para acceder al recurso.
- `500 Internal Server Error`: Se produjo un error al guardar la canción.

### Obtener todas las canciones
```
GET /songs/
```
Este endpoint devuelve una lista de todas las canciones.

#### Respuesta
- `200 OK`: La lista de canciones se ha obtenido correctamente.
- `500 Internal Server Error`: Se produjo un error al obtener las canciones.

### Obtener una canción por ID
```
GET /songs/{id}
```
Este endpoint permite obtener información de una canción específica según su ID.

#### Parámetros de entrada
- `id`: ID de la canción.

#### Respuestas
- `200 OK`: La canción se ha encontrado y se devuelve su información.
- `404 Not Found`: La canción no se encontró en la base de datos.

### Eliminar una canción
```
DELETE /songs/{id}
```
Este endpoint permite eliminar una canción según su ID. Se requiere autenticación con un token válido.

#### Parámetros de entrada
- `id`: ID de la canción a eliminar.

#### Respuestas
- `200 OK`: La canción se ha eliminado correctamente.
- `404 Not Found`: La canción no se encontró en la base de datos.
- `401 Unauthorized`: Se requiere autenticación para acceder al recurso.
- `500 Internal Server Error`: Se produjo un error al eliminar la canción.

### Actualizar una canción
```
PUT /songs/{id}
```
Este endpoint permite actualizar la información de una canción según su ID. Se requiere autenticación con un token válido.

#### Parámetros de entrada
- `id`: ID de la canción a actualizar.
- `name` (opcional): Nuevo nombre de la canción.
- `author` (opcional): Nuevo autor de la canción.
- `genre` (opcional): Nuevo género de la canción.

#### Respuestas
- `200 OK`: La canción se ha actualizado correctamente.
- `400 Bad Request`: Los datos de la solicitud son inválidos.
- `404 Not Found`: La canción no se encontró en la base de datos.
- `401 Unauthorized`: Se requiere autenticación para acceder al recurso.
- `500 Internal Server Error`: Se produjo un error al actualizar la canción.

## Endpoints de Playlists

### Agregar una nueva playlist
```
POST /playlists/
```
Este endpoint permite agregar una nueva playlist. Se requiere autenticación con un token válido.

#### Parámetros de entrada
- `name`: Nombre de la playlist.
- `song_ids` (opcional): Lista de IDs de canciones para agregar a la playlist.

#### Respuestas
- `201 Created`: La playlist se ha creado correctamente.
- `400 Bad Request`: Los datos de la solicitud son inválidos o faltan campos requeridos.
- `401 Unauthorized`: Se requiere autenticación para acceder al recurso.
- `500 Internal Server Error`: Se produjo un error al crear la playlist.

### Obtener todas las playlists
```
GET /playlists/
```
Este endpoint devuelve una lista de todas las playlists.

#### Respuesta
- `200 OK`: La lista de playlists se ha obtenido correctamente.
- `500 Internal Server Error`: Se produjo un error al obtener las playlists.

### Obtener playlists del usuario actual
```
GET /playlists/myPlaylists
```
Este endpoint devuelve una lista de las playlists pertenecientes al usuario actual. Se requiere autenticación con un token válido.

#### Respuesta
- `200 OK`: La lista de playlists se ha obtenido correctamente.
- `401 Unauthorized`: Se requiere autenticación para acceder al recurso.
- `500 Internal Server Error`: Se produjo un error al obtener las playlists.

### Obtener una playlist por ID
```
GET /playlists/{id}
```
Este endpoint permite obtener información de una playlist específica según su ID.

#### Parámetros de entrada
- `id`: ID de la playlist.

#### Respuestas
- `200 OK`: La playlist se ha encontrado y se devuelve su información.
- `403 Forbidden`: Acceso denegado. El usuario no es propietario de la playlist.
- `404 Not Found`: La playlist no se encontró en la base de datos.

### Eliminar una playlist
```
DELETE /playlists/{id}
```
Este endpoint permite eliminar una playlist según su ID. Se requiere autenticación con un token válido.

#### Parámetros de entrada
- `id`: ID de la playlist a eliminar.

#### Respuestas
- `200 OK`: La playlist se ha eliminado correctamente.
- `403 Forbidden`: Acceso denegado. El usuario no es propietario de la playlist.
- `404 Not Found`: La playlist no se encontró en la base de datos.
- `500 Internal Server Error`: Se produjo un error al eliminar la playlist.

### Actualizar una playlist
```
PUT /playlists/{id}
```
Este endpoint permite actualizar la información de una playlist según su ID. Se requiere autenticación con un token válido.

#### Parámetros de entrada
- `id`: ID de la playlist a actualizar.
- `name`: Nuevo nombre de la playlist.

#### Respuestas
- `200 OK`: La playlist se ha actualizado correctamente.
- `400 Bad Request`: Los datos de la solicitud son inválidos.
- `403 Forbidden`: Acceso denegado. El usuario no es propietario de la playlist.
- `404 Not Found`: La playlist no se encontró en la base de datos.
- `500 Internal Server Error`: Se produjo un error al actualizar la playlist.

### Agregar canciones a una playlist
```
POST /playlists/{id}/songs
```
Este endpoint permite agregar canciones a una playlist según su ID. Se requiere autenticación con un token válido.

#### Parámetros de entrada
- `id`: ID de la playlist.
- `song_ids`: Lista de IDs de canciones para agregar a la playlist.

#### Respuestas
- `200 OK`: Las canciones se han agregado a la playlist correctamente.
- `400 Bad Request`: Los datos de la solicitud son inválidos o faltan campos requeridos.
- `403 Forbidden`: Acceso denegado. El usuario no es propietario de la playlist.
- `404 Not Found`: La playlist no se encontró en la base de datos.
- `500 Internal Server Error`: Se produjo un error al agregar las canciones a la playlist.

### Eliminar una canción

 de una playlist
```
DELETE /playlists/{playlist_id}/songs/{song_id}
```
Este endpoint permite eliminar una canción de una playlist según su ID. Se requiere autenticación con un token válido.

#### Parámetros de entrada
- `playlist_id`: ID de la playlist.
- `song_id`: ID de la canción a eliminar.

#### Respuestas
- `200 OK`: La canción se ha eliminado de la playlist correctamente.
- `403 Forbidden`: Acceso denegado. El usuario no es propietario de la playlist.
- `404 Not Found`: La playlist o la canción no se encontraron en la base de datos.
- `500 Internal Server Error`: Se produjo un error al eliminar la canción de la playlist.
