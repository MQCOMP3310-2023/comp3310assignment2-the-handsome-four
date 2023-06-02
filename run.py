from project import create_app
# Debug needs to be removed before the webpage goes live
if __name__ == '__main__':
  app = create_app()
  app.run(host = '0.0.0.0', port = 8000, debug=False)
