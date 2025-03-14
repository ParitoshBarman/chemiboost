// add new item by clicking enter
document.addEventListener("keyup", (e)=>{
    if(e.key === "Enter"){
        addRow();
    }
    else if(e.key === "ArrowUp"){
        try{
        document.getElementById("customer").focus();
    }
    catch{
            document.getElementById("party").focus();
        }
    }
});