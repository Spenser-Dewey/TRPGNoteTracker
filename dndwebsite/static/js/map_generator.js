window.addEventListener("load", () => { generateMap() });

function generateMap() {
    var svg_doc = document.getElementById('map').contentDocument;

    // Insert stylesheets into svg
    let stylesheets = document.head.querySelectorAll("link[rel=stylesheet]");
    for (var i = 0; i < stylesheets.length; i++) {
        var styleLink = svg_doc.createElementNS("http://www.w3.org/1999/xhtml", "link");
        styleLink.setAttribute("href", stylesheets[i].href);
        styleLink.setAttribute("type", "text/css");
        styleLink.setAttribute("rel", "stylesheet");
        svg_doc.querySelector("defs").appendChild(styleLink);
    }

    const country_list = JSON.parse(document.getElementById('map-data').textContent);
    if (document.getElementById('country').textContent != "\"\"") {
        const chosen_country = JSON.parse(document.getElementById('country').textContent);
        generateMapForRegion(svg_doc, chosen_country);
    } else {
        generateFullMap(svg_doc, country_list);
    }
}

function generateMapForRegion(svg_doc, region) {

    labels = svg_doc.querySelector("#labels").querySelector("#states").querySelectorAll("text");
    let fullName = "";
    let regionName = "";
    for (let countryLabel of labels) {
        let labelText = countryLabel.textContent
        if (labelText.toLowerCase().indexOf(region.toLowerCase()) >= 0) {
            fullName = labelText;
            regionName = countryLabel.getAttribute("id").replace(/(state)label(\d+)/i, "$1$2")
            found = true;
            /// Remove region label, make page title be the region title
            countryLabel.remove();
            document.querySelector("#title").textContent = fullName;
            break;
        }
    }
    if (!found) {
        message = "Country: \"" + region + "\" is not in the SVG we loaded! Something must have gone wrong with the map upload...";
        alert(message);
        return;
    }
    let svgRegion;
    try {
        svgRegion = svg_doc.querySelector("#" + regionName).getBBox();
    } catch (error) {
        alert("SVG is not formatted the way the site expects! SVG should have stateLabel#, and state#");
        return;
    }

    // Clip everythin except the country, scale the country size up to match the original map's height
    const REGION_SCALE_FACTOR = svg_doc.querySelector("svg").getAttribute("height") / svgRegion.height;

    const countryMask = document.createElementNS("http://www.w3.org/2000/svg", "mask");
    const maskRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    maskRect.setAttribute("fill", "white");
    maskRect.setAttribute("x", svgRegion.x);
    maskRect.setAttribute("y", svgRegion.y);
    maskRect.setAttribute("width", svgRegion.width);
    maskRect.setAttribute("height", svgRegion.height);
    countryMask.setAttribute("id", "country_mask");
    countryMask.appendChild(maskRect);
    svg_doc.querySelector("#deftemp").appendChild(countryMask);
    svg_doc.querySelector("#viewbox").setAttribute("mask", "url(#country_mask)");
    svg_doc.querySelector("#viewbox").setAttribute("transform", "translate(" + (-REGION_SCALE_FACTOR * svgRegion.x) + " " + (-REGION_SCALE_FACTOR * svgRegion.y)
        + ") scale( " + REGION_SCALE_FACTOR + " " +  REGION_SCALE_FACTOR + ")");

    svg_doc.querySelector("#labels").querySelector("#cities").setAttribute("font-size", "7");
    svg_doc.querySelector("#labels").querySelector("#cities").setAttribute("style", "");
    svg_doc.querySelector("#labels").querySelector("#towns").setAttribute("font-size", "4");
    svg_doc.querySelector("#labels").querySelector("#towns").setAttribute("style", "");

    svg_doc.querySelector("#scaleBar").remove();
    svg_doc.querySelector("svg").setAttribute("width", "" + REGION_SCALE_FACTOR * svgRegion.width);
}

function generateFullMap(svg_doc, country_list) {
    // Create popup box and components
    const popup_box = document.createElementNS("http://www.w3.org/2000/svg", "g");
    constructPopup(popup_box, country_list);
    svg_doc.querySelector("#viewbox").appendChild(popup_box);
    popup_bounding_box = popup_box.getBoundingClientRect();
    canvas_bounding_box = document.querySelector("#map").getBoundingClientRect();

    // Create popup triggers
    popup_box.addEventListener('focusout', function (event) {
        popup_box.setAttribute("visibility", "hidden");
    });

    labels = svg_doc.querySelector("#labels").querySelector("#states").querySelectorAll("text");
    labels.forEach((label) => label.addEventListener('click', function (event) {
        let message = "";
        point = DOMPoint.fromPoint({ 'x': event.x, 'y': event.y })
        let hovered_country = label.textContent
        let found = false;
        for (let country in country_list) {
            if (hovered_country.toLowerCase().indexOf(country.toLowerCase()) >= 0) {
                hovered_country = country;
                found = true;
                break;
            }
        }
        if (!found) {
            message = "Country: \"" + hovered_country + "\" is not in our database! Something must have gone wrong with the map upload...";
            popup_box.querySelector("#country_more_info_btn").setAttribute("visibility", "hidden");
        } else {
            message = hovered_country + " is the nicest place you'll every go... if you seek your own death! Bah bah bummm!! Extended message, going on and on, the mountains are lovely, the rivers refreshing, the seaside views transformational, the gods fickle..."
            popup_box.querySelector("#country_more_info_btn").setAttribute("visibility", "default");
        }
        let message_box = popup_box.querySelector("#swappable_popup_text");
        if (message_box) {
            message_box.remove();
        }
        popup_box.querySelector("#country_header").innerHTML = hovered_country;
        message_box = breakText(message, 70, "1.0rem");
        message_box.setAttribute("id", "swappable_popup_text");
        message_box.setAttribute("transform", "translate(0.0 30.0)");
        if (point.x + popup_bounding_box.width > canvas_bounding_box.width) {
            point.x = canvas_bounding_box.width - popup_bounding_box.width;
        }
        if (point.y + popup_bounding_box.height > canvas_bounding_box.height) {
            point.y = canvas_bounding_box.height - popup_bounding_box.height;
        }
        popup_box.setAttribute('transform', "translate(" + point.x + " " + point.y + ")");
        popup_box.setAttribute("visibility", "visible");
        popup_box.appendChild(message_box);
        popup_box.focus();
    }));
}

// Break text into multiple lines
function breakText(text, width, lineheight) {
    let words = text.split(' ');
    let nextLine = words[0] + ' ';

    let textblock = document.createElementNS("http://www.w3.org/2000/svg", "text");
    let charCount;
    for (let i = 1; i < words.length; i++) {
        let testLine = nextLine + words[i] + ' ';
        charCount = testLine.length;
        if (charCount > width) {
            let svgLine = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
            svgLine.setAttribute("dy", lineheight);
            svgLine.setAttribute("x", "0");
            svgLine.innerHTML = nextLine;
            textblock.appendChild(svgLine);

            nextLine = words[i] + ' ';
            charCount = 0;
        } else {
            nextLine = testLine;
        }
    }
    // Add final line
    let svgLine = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
    svgLine.setAttribute("dy", lineheight);
    svgLine.setAttribute("x", "0");
    svgLine.innerHTML = nextLine;
    textblock.appendChild(svgLine);

    return textblock;
}

function constructPopup(popup_box, country_list) {
    const popup_bg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    popup_bg.classList += "popup";
    popup_bg.setAttribute('width', "30rem");
    popup_bg.setAttribute('height', "10rem");
    const header = document.createElementNS("http://www.w3.org/2000/svg", "text");
    header.setAttribute("class", "popup_header");
    header.setAttribute("id", "country_header");
    header.innerHTML = "HEADER";
    header.setAttribute('x', "0rem");
    header.setAttribute('y', "1rem");
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("class", "popup_separator");
    line.setAttribute("x1", "0rem");
    line.setAttribute("y1", "1.5rem");
    line.setAttribute("x2", "5rem");
    line.setAttribute("y2", "1.5rem");
    const more_info_rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    more_info_rect.classList += "popup_info_btn";
    more_info_rect.setAttribute('width', "6.5rem");
    more_info_rect.setAttribute('height', "2rem");
    more_info_rect.setAttribute('x', '23.5rem');
    more_info_rect.setAttribute('y', '8rem');
    const more_info_txt = document.createElementNS("http://www.w3.org/2000/svg", "text");
    more_info_txt.setAttribute("x", "24.5rem");
    more_info_txt.setAttribute("y", "9.6rem");
    more_info_txt.innerHTML = "More Info...";

    const popupBtn = document.createElementNS("http://www.w3.org/2000/svg", "g");
    popupBtn.setAttribute("id", "country_more_info_btn");
    popupBtn.appendChild(more_info_rect);
    popupBtn.appendChild(more_info_txt);
    popupBtn.addEventListener('click', (event) => {
        window.location.href = country_list[header.innerHTML];
    });


    popup_box.appendChild(popup_bg);
    popup_box.appendChild(header);
    popup_box.appendChild(line);
    popup_box.appendChild(popupBtn);

    popup_box.setAttribute("visibility", "hidden");
    popup_box.setAttribute("id", "country_popup");

}