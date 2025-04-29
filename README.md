# Face-Authorization

## Overview

Face-Authorization is a project that provides an API for facial recognition-based authorization. It allows clients to submit images (typically as base64-encoded strings or image files) and receive a response indicating whether the face matches an authorized user.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/iamvrajpatel/Face-Authorization.git
   cd Face-Authorization
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   - If using Flask:
     ```bash
     python app.py
     ```
   - If using another framework, refer to the main entry point (e.g., `main.py`).

4. **API will be available at:**
   ```
   http://localhost:5000/
   ```

## Notes

- Ensure your input image is clear and contains only one face for best results.
- The API may require a pre-populated database of authorized faces. Refer to project documentation for enrollment procedures if available.


# Face Verification API

This API endpoint is used to verify and compare two face images by sending a `POST` request with the URLs of the registered image and the test image in the raw request body.

## 📌 **Endpoint**
```
POST /face-verification
```

## 🔹 **Request Body**

The request body should be in JSON format and must include the URLs of the registered image and the test image.

| Parameter       | Type   | Required | Description |
|---------------|--------|----------|-------------|
| `reg_image_url`  | `string` | ✅ | The URL of the registered image. |
| `test_image_url` | `string` | ✅ | The URL of the test image to be verified. |
| `criteria` (optional) | `integer` | ❌ | The threshold percentage for face matching (default: `75%`). |

### **Example Request JSON**
```json
{
    "reg_image_url": "<image-url>",
    "test_image_url": "<image-url>"
}
```

---

## 🔹 **Response**
Upon successful verification, the API returns a status code of `200` and a JSON response with the verification result.

| Field               | Type    | Description |
|---------------------|---------|-------------|
| `match`            | `boolean` | `true` if the faces match, otherwise `false`. |
| `confidence_percent` | `float`   | The confidence level of the match (percentage). |

### **Example Response JSON**
```json
{
    "match": true,
    "confidence_percent": 100.0
}
```

---

## 📌 **Error Handling**
If the request is invalid or an error occurs during processing, the API will return an appropriate HTTP status code with an error message.

| HTTP Status Code | Description |
|------------------|-------------|
| `400 Bad Request` | Missing or invalid parameters in the request body. |
| `500 Internal Server Error` | An unexpected error occurred while processing the request. |

---

## 📌 **Usage Example**
### **Using `cURL`**
```sh
curl -X POST https://your-api-url.com/face-verification \
     -H "Content-Type: application/json" \
     -d '{
         "reg_image_url": "<image-url>",
         "test_image_url": "<image-url>"
     }'
```

---

## 🔹 **Notes**
- If `criteria` is not provided, the default matching confidence threshold is `75%`.
- Make sure the image URLs are publicly accessible.
- The response time may vary depending on the image size and network latency.

---

## License

MIT License