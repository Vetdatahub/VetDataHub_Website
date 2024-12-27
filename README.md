
# VetDataHub_Website

![VetDataHub Logo](./2f870ea104fe8e3fe891bf40e9ecf6a5.jpg) 

**VetDataHub** is an open-source veterinary dataset repository aimed at facilitating the sharing and exchange of diverse datasets in the veterinary field. The platform is designed to handle large datasets efficiently, support collaboration among researchers and practitioners, and provide tools for exploring and contributing to datasets.

## Features

- **Dataset Hosting:** Easily upload and host your veterinary datasets.
- **Metadata Management:** Manage metadata for each dataset, including descriptions, keywords, and more.
- **Search Functionality:** Quickly search for datasets based on keywords and filters.
- **API Access:** Access datasets programmatically through a well-documented API.
- **Community Discussions:** Engage with other users in community discussion forums.
- **Version Control:** Keep track of different versions of datasets and revert if necessary.
- **Rating and Reviews:** Rate datasets and leave reviews to help others in the community.
- **User Profiles:** Create profiles showcasing your contributions and activity on the platform.
- **Responsive Design:** Access the platform on any device with a mobile-friendly design.

## Installation

To set up the VetDataHub locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/VetDataHub_Website.git
   cd vetdatahub
   ```

2. **Install dependencies:**
   Make sure you have Python and pip installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   Configure your database settings in the `settings.py` file, which you can find in the ``vetdatahub``, folder and run:
   ```bash
   python manage.py migrate
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000`.

## Usage

Once the application is running, you can:

- **Create an account** to upload datasets and engage with the community.
- **Browse datasets** by categories or use the search functionality.
- **Participate in discussions** and provide feedback on datasets.
- **Access the API** for programmatic access to datasets.

## Commmunity 
You can join the VetDataHub community on discord [here](https://discord.gg/XEKB767wgT)

## Contributing

We welcome contributions to improve VetDataHub! To contribute:
[Read](./CONTRIBUTING.md)

## 🙇‍♂️ Acknowledgments

<p>This project is proudly supported by:</p>
<p>
  <a href="https://www.digitalocean.com/">
    <img src="https://opensource.nyc3.cdn.digitaloceanspaces.com/attribution/assets/SVG/DO_Logo_horizontal_blue.svg" width="201px">
  </a>
</p>
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please reach out:

- **Project Lead:** [Johanan Oppong Amoateng](mailto:johananoppongamoateng2001@gmail.com)
- **GitHub:** [JohananOppongAmoateng](https://github.com/JohananOppongAmoateng)
