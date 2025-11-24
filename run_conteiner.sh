
#!/usr/bin/env bash

# Detect docker compose command (POSIX-friendly)
USE_DOCKER_COMPOSE=0
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
	USE_DOCKER_COMPOSE=1
elif command -v docker-compose >/dev/null 2>&1; then
	USE_DOCKER_COMPOSE=0
else
	echo "No docker compose command found. Aborting."
	exit 1
fi

# Helper to run compose commands portably
run_compose() {
	if [ "$USE_DOCKER_COMPOSE" -eq 1 ]; then
		docker compose "$@"
	else
		docker-compose "$@"
	fi
}

# Stop any previous containers if they exist
echo "Cleaning up previous containers..."
run_compose down 2>/dev/null || true

# Build and start containers
echo "Building and starting containers..."
run_compose up --build -d

echo "Waiting for services to be ready..."
sleep 5

# Check container status
echo ""
echo "Containers status:"
docker ps --filter "name=docker-compose-down-advanced" --filter "name=postgres-db-3-advanced"

echo ""
echo "Containers started!"
echo ""
echo "Running migrations..."
docker exec docker-compose-down-advanced python manage.py migrate

echo ""
echo "Loading initial data (fixtures)..."
docker exec docker-compose-down-advanced python manage.py loaddata ex00/fixtures/initial_data.json

echo ""
echo "Creating superuser (if not exists)..."
docker exec docker-compose-down-advanced python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" 2>/dev/null

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Available URLs:"
echo "  - Articles:      http://localhost:8000"
echo "  - Login:         http://localhost:8000/login/"
echo "Admin User:"
echo "  - admin / admin123"
echo "  - password: HelloSalutHola"
echo ""
echo "To start the Django server, run inside the container:"
echo "  python manage.py runserver 0.0.0.0:8000"
echo ""

# Open a shell in the Django container
docker exec -it docker-compose-down-advanced /bin/zsh