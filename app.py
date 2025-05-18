from app import create_app

# Create an app instance using the factory method
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Allow access on all network interfaces