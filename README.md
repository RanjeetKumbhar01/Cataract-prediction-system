# CataractAI 👁️

# Deployed Project: [Hugging Face: CataractAI](https://huggingface.co/spaces/Ranjeet-Potter/CataractAI-Cataract-Prediction-System)

CataractAI is a platform designed for medical staff and patients to facilitate the early detection of cataracts. The platform enables users to sign up, log in, and upload Fundus images. The uploaded images are analyzed using a deep learning model, EfficientNetB0, pre-trained on ImageNet, to determine whether cataracts are present or not.

## Features 📖

- **User Roles**:

  **Patients**: Register, log in, and upload Fundus images for cataract detection.

  **Medical Staff**: Register with hospital details, log in, and manage Fundus image uploads.

- **AI-Powered Detection**: Utilizes the EfficientNetB0 model trained on ImageNet weights for high-accuracy predictions.
- **Secure Authentication**: Passwords are hashed using bcrypt for enhanced security.
- **User-Friendly Interface**: HTML templates render a clean and easy-to-navigate frontend.

## Tech Stack 🤖

- **Backend**: Flask
- **Database**: MySQL
- **Machine Learning**: TensorFlow (EfficientNet-B0 model with ImageNet weights)
- **Frontend**: Basic HTML and CSS

## Installation 📦

### Prerequisites

- Python 3.7 or higher
- MySQL Server

### Steps

**1. Clone the repository:**

        git clone https://github.com/your-repo/CataractAI.git
        cd CataractAI

**2. Install dependencies:**

        pip install -r requirements.txt

**3. Configure MySQL:**

- Create a database named user_management.
- Run the following SQL script to create the required table:

        CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        age INT,
        user_type ENUM('patient', 'staff'),
        hospital_name VARCHAR(255) );

**4. Run the application:**

        python app.py

## Contributing 🤝!

We welcome contributions from the community! If you would like to contribute, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

# License 📜

This project is licensed under the MIT. Feel free to use the code and materials for educational purposes or personal projects.

# Contact ✉️

If you have any questions or suggestions, please feel free to contact:

- Email: Ranjeet - **contact [dot] ranjeetkumbhar [at] gmail [dot] com**

---

Thank you for using CataractAI! We hope this tool helps in the early detection and treatment of cataracts. If you have any feedback or need assistance, please do not hesitate to reach out.

Happy coding!

![](https://github.com/RanjeetKumbhar01/Cataract-prediction-system/blob/main/static/BabyYodaGroguGIF.gif)
