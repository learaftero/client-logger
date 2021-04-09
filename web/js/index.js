const addNewMember = document.getElementById("add-member");
const clintTabDiv = document.getElementById("tab-div");
const calender = document.getElementById("start");
// const cloneDataBaseTable = document.getElementById("search-month-year");
const cloneForm = document.getElementById("query-form");

// Event Handlers
//---------------
window.addEventListener("load", () => {
    addYearAndMonth();
    getDataToCreatClintDashboard();
});

addNewMember.addEventListener("click", addMember);
clintTabDiv.addEventListener("click", allEventListenerTab);
// Search for the month/year
// searchBtn.addEventListener("click", searchDataForMonthAndYear);
calender.addEventListener("input", searchDataForMonthAndYear);
cloneForm.addEventListener("submit", cloneDataBase);

// one time Event Handlers
// -----------------------
// Add New Member button action
document.getElementById("member-add").addEventListener("click", function () {
    document.querySelectorAll(".bg-modal")[0].style.display = "flex";
    document.body.classList.toggle("body-scroll-lock");
});
// Add New Member close action
document.getElementById("close").addEventListener("click", function () {
    document.querySelectorAll(".bg-modal")[0].style.display = "none";
    document.body.classList.toggle("body-scroll-lock");
});
// for cloning the data base
document.getElementById("search-btn").addEventListener("click", function () {
    document.querySelectorAll(".bg-modal")[1].style.display = "flex";
    document.body.classList.toggle("body-scroll-lock");
});
document.getElementById("close-query").addEventListener("click", function () {
    document.querySelectorAll(".bg-modal")[1].style.display = "none";
    document.body.classList.toggle("body-scroll-lock");
});

// Functions

function addYearAndMonth() {
    // Add current month and year to the month and year selector.
    const setMonthYear = document.getElementById("start");
    eel.get_current_date()().then(date => {
        setMonthYear.value = date;
        console.log(date);
    });
}

function getDataToCreatClintDashboard() {
//    Makes a call to the database.
    eel.get_the_query_data_from_database()().then(rowData => {
        rowData.forEach(data => {
            addNewMemberToDashboard(data)
        })
    });
}

function searchDataForMonthAndYear() {
    let searchValue = calender.value;
    let oldDiv = document.querySelector(".content-row");
    eel.search_for_table(searchValue)().then(data => {
        if (data === false) {
            alert("Error message : unknown month or year is given.\nPlease change the values and try again");
        } else {
            oldDiv.innerHTML = "";
            data.forEach(data => {
                addNewMemberToDashboard(data)
            })
        }
    })
}

function addMember(event) {
    event.preventDefault();
    let form = document.getElementsByClassName("form");
    let fdObject = {};
    let fD = new FormData(form[0]);
    for (let pair of fD.entries()) {
        fdObject[pair[0]] = pair[1] === "" ? "-----/-----" : pair[1];
    }
    console.log(fdObject);
    document.querySelector(".bg-modal").style.display = "none";
    sendFormDataToPython(fdObject);
    document.body.classList.toggle("body-scroll-lock");
}

function addNewMemberToDashboard(data) {
    let div = document.createElement("div");
    div.classList.add("slot", "grid-style");
    div.id = data["rowid"];
    // name label
    let nameLabel = document.createElement("label");
    nameLabel.classList.add("clint-name");
    nameLabel.innerText = data["name"];
    div.appendChild(nameLabel);
    // Filling task
    let taskImag = document.createElement("span");
    taskImag.classList.add("icon-style", data["filling_state"] === "yes" ? "item-complete" : null);
    taskImag.innerHTML = '<img src="./img/icons/task.png" alt="filling_state" />';
    div.appendChild(taskImag);
    // payment
    let rupeeImag = document.createElement("span");
    rupeeImag.classList.add("icon-style", data["payment_state"] === "yes" ? "item-complete" : null);
    rupeeImag.innerHTML = '<img src="./img/icons/rupee.png" alt="payment_state" />';
    div.appendChild(rupeeImag);
    // GSTIN
    let gstin = document.createElement("label");
    gstin.innerText = data["gstin"];
    div.appendChild(gstin);
    // Company states
    let company = document.createElement("label");
    company.innerText = data["company_name"];
    div.appendChild(company);
    // hidden content
    let hiddenDiv = document.createElement("div");
    hiddenDiv.classList.add("hidden", "hidden-style");
    hiddenDiv.innerHTML = `
    <div>
        <label>Login ID:</label>
        <label>${data["gstin_login_id"]}</label>
    </div>
    <div>
        <label>Login Password:</label>
        <label>${data["gstin_password"]}</label>
    </div>`;
    div.appendChild(hiddenDiv);
    // Delete button
    let deleteBtn = document.createElement("button");
    deleteBtn.innerHTML = "<span class='delete-btn material-icons'> delete_forever </span>";
    div.appendChild(deleteBtn);
    // appending every thing to the parent div
    let contentDiv = document.querySelector(".content-row");
    contentDiv.appendChild(div)
}

function sendFormDataToPython(data) {
    eel.get_data_from_js(data)().then(clintDashboardRow => {
        addNewMemberToDashboard(clintDashboardRow)
    });
}

function allEventListenerTab(e) {
    if (e.target !== e.currentTarget) {
        let item = e.target;
        let parentDiv = item.parentElement;
        let divChildren = parentDiv.children;
        let grandParentsDiv = parentDiv.parentElement;
        let rowId = grandParentsDiv.id;
        if (e.target.classList[0] === "clint-name") {
            divChildren[5].classList.toggle("hidden");
            parentDiv.classList.toggle("div-style")
        }
        if (item.classList[0] === "delete-btn") {
            // let deleteConfirm =  confirm("Are you sure you want to delete the clint tab.\nThis process cannot be undone.");
            // if (deleteConfirm){
            // }
            //-------------
            grandParentsDiv.classList.add("delete-transition");
            grandParentsDiv.addEventListener("transitionend", function () {
                grandParentsDiv.remove();
            });
            eel.delete_row(rowId);
        }
        if (parentDiv.classList[0] === "icon-style") {
            if (parentDiv.classList.toggle("item-complete")) {
                console.log(item.alt);
                const rowItem = [item.alt, "yes"];
                eel.update_row_item(rowItem, rowId)
            } else {
                console.log("no");
                const rowItem = [item.alt, "no"];
                eel.update_row_item(rowItem, rowId)
            }
            console.log(item)
        }
        // console.log(parentDiv.classList[0] === "icon-style");
    }
    e.stopPropagation();
}

function cloneDataBase(event) {
    event.preventDefault();
    let fbObject = {};
    let fd = new FormData(cloneForm);
    for (let pair of fd.entries()) {
        fbObject[pair[0]] = pair[1] === "" ? "-----/-----" : pair[1];
    }
    document.querySelectorAll(".bg-modal")[1].style.display = "none";
    document.body.classList.toggle("body-scroll-lock");
    cloneForm.reset();
    console.log(fbObject,"hello");
    eel.clone_data_base(fbObject);
}