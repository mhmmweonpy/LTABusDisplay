import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize, Qt

class BusTimingUI(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window properties
        self.setWindowTitle("Bus Timing Display")
        self.setGeometry(100, 100, 480, 320)  # Screen size for 3.5-inch TFT

        # Set up the main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Add refresh button at the top
        self.add_top_bar()

        # Add bus stops sections
        self.add_bus_stop("Blk 137", "67129", [
            {"number": "50", "times": ["2", "9", "15"], "loads": [False, False, False], "doubles": [False, False, False]},
            {"number": "119", "times": ["15", "9", "15"], "loads": [False, False, False], "doubles": [True, False, False]},
            {"number": "136", "times": ["Arriving", "9", "15"], "loads": [False, False, False], "doubles": [True, False, True]}
        ])
        self.add_bus_stop("Blk 142A", "67121", [
            {"number": "50", "times": ["2", "9", "15"], "loads": [False, False, False], "doubles": [True, True, True]},
            {"number": "119", "times": ["15", "9", "15"], "loads": [True, True, True], "doubles": [True, True, True]},
            {"number": "136", "times": ["15", "9", "15"], "loads": [True, True, True], "doubles": [True, True, True]}
        ])

    def add_top_bar(self):
        # Top bar layout
        top_layout = QHBoxLayout()

        # Add refresh button (SVG icon)
        refresh_icon = QSvgWidget()
        refresh_icon.load(bytearray(self.refresh_svg(), encoding='utf-8'))
        refresh_icon.setFixedSize(30, 30)
        top_layout.addStretch()
        top_layout.addWidget(refresh_icon)

        self.main_layout.addLayout(top_layout)

    def add_bus_stop(self, stop_name, stop_code, buses):
        # Add bus stop layout
        stop_layout = QVBoxLayout()

        # Bus stop header
        stop_header = QLabel(f"{stop_name}\n{stop_code}")
        stop_header.setFont(QFont('Arial', 16))
        stop_layout.addWidget(stop_header)

        # Add buses in this stop
        for bus in buses:
            self.add_bus_row(bus, stop_layout)

        self.main_layout.addLayout(stop_layout)

    def add_bus_row(self, bus, stop_layout):
        # Create a horizontal layout for each bus row (with 3 timings horizontally)
        row_layout = QHBoxLayout()

        # Bus number
        bus_number = QLabel(bus["number"])
        bus_number.setFont(QFont('Arial', 24))
        row_layout.addWidget(bus_number)

        # Add the next 3 bus timings
        for i in range(3):
            timing_layout = QVBoxLayout()

            # Bus arrival time
            bus_time = QLabel(f"{bus['times'][i]} mins" if bus['times'][i] != "Arriving" else "Arriving")
            bus_time.setFont(QFont('Arial', 16))
            timing_layout.addWidget(bus_time)

            # Load availability icon (cross and person icon if full)
            if not bus["loads"][i]:
                cross_icon = QSvgWidget()
                cross_icon.load(bytearray(self.cross_svg(), encoding='utf-8'))
                cross_icon.setFixedSize(14, 14)

                person_icon = QSvgWidget()
                person_icon.load(bytearray(self.person_svg(), encoding='utf-8'))
                person_icon.setFixedSize(14, 20)

                timing_layout.addWidget(cross_icon)
                timing_layout.addWidget(person_icon)

            # Double-decker bus icon
            if bus["doubles"][i]:
                bus_icon = QSvgWidget()
                bus_icon.load(bytearray(self.bus_svg(), encoding='utf-8'))
                bus_icon.setFixedSize(15, 15)
                timing_layout.addWidget(bus_icon)

            # Add the timing layout to the row
            row_layout.addLayout(timing_layout)

        stop_layout.addLayout(row_layout)

    def refresh_svg(self):
        return """
        <svg xmlns="http://www.w3.org/2000/svg" width="29.25" height="29.25" viewBox="0 0 29.25 29.25">
          <path id="Refresh" d="M18,3.375A14.625,14.625,0,1,0,32.625,18,14.642,14.642,0,0,0,18,3.375Zm0,22.008a6.609,6.609,0,0,1,0-13.219h.3l-.992-.991A.984.984,0,1,1,18.7,9.78l2.813,2.812a.984.984,0,0,1,0,1.392L18.7,16.8A.984.984,0,1,1,17.3,15.405L18.57,14.14c-.167-.007-.359-.007-.57-.007a4.641,4.641,0,1,0,4.641,4.641.984.984,0,0,1,1.969,0A6.617,6.617,0,0,1,18,25.383Z" fill="#fff"/>
        </svg>
        """

    def bus_svg(self):
        return """
        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 15 15">
          <path id="Icon_fa-solid-bus" d="M9.75,0c3.937,0,6.563,1.031,6.563,2.344V3.75a.936.936,0,0,1,.938.938V6.563a.936.936,0,0,1-.937.938v4.688a.936.936,0,0,1-.937.938v.938a.936.936,0,0,1-.937.938H13.5a.936.936,0,0,1-.937-.937v-.937H6.938v.938A.936.936,0,0,1,6,15H5.063a.936.936,0,0,1-.937-.937v-.937a.936.936,0,0,1-.937-.937V7.5a.936.936,0,0,1-.937-.937V4.688a.936.936,0,0,1,.938-.938V2.344C3.188,1.031,5.813,0,9.75,0ZM5.063,4.688V7.5A.936.936,0,0,0,6,8.438H9.281V3.75H6A.936.936,0,0,0,5.063,4.688Zm5.156,3.75H13.5a.936.936,0,0,0,.938-.937V4.688A.936.936,0,0,0,13.5,3.75H10.219ZM5.531,11.719a.938.938,0,1,0-.937-.937A.938.938,0,0,0,5.531,11.719Zm8.438,0a.938.938,0,1,0-.937-.937A.938.938,0,0,0,13.969,11.719ZM12.563,2.344a.47.47,0,0,0-.469-.469H7.406a.469.469,0,0,0,0,.938h4.687A.47.47,0,0,0,12.563,2.344Z" fill="#fff"/>
        </svg>
        """

    def cross_svg(self):
        return """
        <svg xmlns="http://www.w3.org/2000/svg" width="14.243" height="14.243" viewBox="0 0 14.243 14.243">
          <path d="M19,9,9,19M9,9,19,19" transform="translate(-6.879 -6.879)" fill="#fff" stroke="#fff" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"/>
        </svg>
        """

    def person_svg(self):
        return """
        <svg xmlns="http://www.w3.org/2000/svg" width="10" height="15.997" viewBox="0 0 10 15.997">
          <path id="Icon_fa-solid-person" d="M3.5,1.5A1.5,1.5,0,1,1,5,3,1.5,1.5,0,0,1,3.5,1.5ZM4.75,11v4a1,1,0,1,1-2,0V8.027L1.857,9.514A1,1,0,1,1,.145,8.483L1.966,5.452A3,3,0,0,1,4.538,4h.928A3,3,0,0,1,8.037,5.452L9.859,8.483A1,1,0,0,1,8.146,9.514l-.9-1.487V15a1,1,0,1,1-2,0V11Z" fill="#fff"/>
        </svg>
        """

# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BusTimingUI()
    window.show()
    sys.exit(app.exec_())
