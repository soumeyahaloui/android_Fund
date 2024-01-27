from flask import Flask, jsonify
import pymysql
import traceback
import logging
import os


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


def get_database_connection() -> pymysql.connections.Connection:
    # Use the details from your cloud database service.
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        db=os.environ.get('DB_NAME'),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        connection = get_database_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM fundr_alx")
            result = cursor.fetchall()
            return jsonify(result)
    except Exception as e:
        logging.error(f"Error: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()
            logging.info("Database connection closed.")


@app.route('/get_family_data/<int:family_id>', methods=['GET'])
def get_family_data(family_id):
    try:
        connection = get_database_connection()
        with connection.cursor() as cursor:
            query = "SELECT * FROM fundr_alx WHERE ID = %s"
            cursor.execute(query, (family_id,))
            result = cursor.fetchone()
            if result:
                return jsonify(result)
            else:
                return jsonify({"error": "Family not found"}), 404
    except Exception as e:
        logging.error(f"Error: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()
            logging.info("Database connection closed.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
