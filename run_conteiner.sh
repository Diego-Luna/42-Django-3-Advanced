
#!/bin/bash

# Stop any previous containers if they exist
echo "Cleaning up previous containers..."
docker compose down 2>/dev/null

# Build and start containers
echo "Building and starting containers..."
docker compose up --build -d

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
echo "  - Home/Articles: http://localhost:8000"
echo "  - Login:         http://localhost:8000/login/"
echo "  - Admin:         http://localhost:8000/admin/"
echo ""
echo "Test Users:"
echo "  - john_doe / test123"
echo "  - jane_smith / test123"
echo "  - bob_wilson / test123"
echo ""
echo "Admin User:"
echo "  - admin / admin123"
echo ""
echo "To start the Django server, run inside the container:"
echo "  python manage.py runserver 0.0.0.0:8000"
echo ""
echo "Opening Django container shell..."
echo ""

# Open a shell in the Django container
docker exec -it docker-compose-down-advanced /bin/zsh