import firebase_admin
from firebase_admin import credentials, firestore

service_account_json = "recalldb-c4b8c-firebase-adminsdk-7o0x7-427e554d16.json"

class FirestoreHandler:
    def __init__(self, collection_name, service_account_path):
        """
        Initialize Firestore client with the Admin SDK and set the collection name.
        :param collection_name: Name of the Firestore collection.
        :param service_account_path: Path to the Firebase Admin SDK service account key file.
        """
        if not firebase_admin._apps:  # Prevent initializing multiple times
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.collection = self.db.collection(collection_name)

    def write_document(self, document_id, data):
        """
        Write data to Firestore with a specific document ID.
        :param document_id: The ID of the document to write.
        :param data: A dictionary containing the data to write.
        """
        self.collection.document(document_id).set(data)
        print(f"Document {document_id} written successfully.")

    def read_document(self, document_id):
        """
        Read data from a specific document in Firestore.
        :param document_id: The ID of the document to read.
        :return: The data as a dictionary, or None if the document doesn't exist.
        """
        doc = self.collection.document(document_id).get()
        if doc.exists:
            print(f"Document {document_id} data: {doc.to_dict()}")
            return doc.to_dict()
        else:
            print(f"Document {document_id} does not exist.")
            return None

    def update_document(self, document_id, data):
        """
        Update specific fields in a document.
        :param document_id: The ID of the document to update.
        :param data: A dictionary containing the fields to update.
        """
        self.collection.document(document_id).update(data)
        print(f"Document {document_id} updated successfully.")

    def read_all_documents(self):
        """
        Read all documents in the collection.
        :return: A list of dictionaries containing document data.
        """
        docs = self.collection.stream()
        all_docs = [{doc.id: doc.to_dict()} for doc in docs]
        print(f"All documents: {all_docs}")
        return all_docs


# Example usage
if __name__ == "__main__":
    # Path to your service account key JSON file
    service_account_path = "path/to/your-service-account-file.json"

    # Initialize FirestoreHandler with a collection name
    firestore_handler = FirestoreHandler("test_collection", service_account_path)

    # Write a document
    firestore_handler.write_document("doc1", {"name": "Alice", "age": 25})

    # Read a document
    firestore_handler.read_document("doc1")

    # Update a document
    firestore_handler.update_document("doc1", {"age": 26})

    # Read all documents
    firestore_handler.read_all_documents()

# st.session_state.firebase_app = firebase_admin.initialize_app(cred)