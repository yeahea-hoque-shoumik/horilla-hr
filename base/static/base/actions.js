tickShiftCheckboxes();
function makeShiftListUnique(list) {
    return Array.from(new Set(list));
}

tickWorkFromCheckboxes();
function makeWorkFromListUnique(list) {
    return Array.from(new Set(list));
}

tickRShiftCheckboxes();
function makeRShiftListUnique(list) {
    return Array.from(new Set(list));
}

tickRWorkFromCheckboxes();
function makeRWorkFromListUnique(list) {
    return Array.from(new Set(list));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(".all-rshift").change(function (e) {
    var is_checked = $(this).is(":checked");
    var closest = $(this)
        .closest(".oh-sticky-table__thead")
        .siblings(".oh-sticky-table__tbody");
    if (is_checked) {
        $(closest)
            .children()
            .find(".all-rshift-row")
            .prop("checked", true)
            .closest(".oh-sticky-table__tr")
            .addClass("highlight-selected");
    } else {
        $(closest)
            .children()
            .find(".all-rshift-row")
            .prop("checked", false)
            .closest(".oh-sticky-table__tr")
            .removeClass("highlight-selected");
    }
});

function tickRShiftCheckboxes() {
    var ids = JSON.parse($("#selectedRShifts").attr("data-ids") || "[]");
    uniqueIds = makeRShiftListUnique(ids);
    toggleHighlight(uniqueIds);
    click = $("#selectedRShifts").attr("data-clicked");
    if (click === "1") {
        $(".all-rshift").prop("checked", true);
    }
    uniqueIds.forEach(function (id) {
        $("#" + id).prop("checked", true);
    });
    var selectedCount = uniqueIds.length;
    if (selectedCount > 0) {
        $("#exportRShifts").css("display", "inline-flex");
        $("#unselectAllRShifts").css("display", "inline-flex");
        $("#selectedShowRShifts").css("display", "inline-flex");
        $("#selectedShowRShifts").text(selectedCount + " -" + i18nMessages.selected);
    } else {
        $("#selectedShowRShifts").css("display", "none");
        $("#exportRShifts").css("display", "none");
        $("#unselectAllRShifts").css("display", "none");
    }
}

$("#exportRShifts").click(function (e) {
    var currentDate = new Date().toISOString().slice(0, 10);
    ids = [];
    ids = JSON.parse($("#selectedRShifts").attr("data-ids"));
    Swal.fire({
        text: i18nMessages.downloadExcel,
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#008000",
        cancelButtonColor: "#6c757d",
        confirmButtonText: i18nMessages.confirm,
        cancelButtonText: i18nMessages.cancel,
    }).then(function (result) {
        if (result.isConfirmed) {
            $.ajax({
                type: "GET",
                url: "/rotating-shift-assign-info-export",
                data: {
                    ids: JSON.stringify(ids),
                },
                dataType: "binary",
                xhrFields: {
                    responseType: "blob",
                },
                success: function (response) {
                    const file = new Blob([response], {
                        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    });
                    const url = URL.createObjectURL(file);
                    const link = document.createElement("a");
                    link.href = url;
                    link.download =
                        "Rotating_shift_assign_export" + currentDate + ".xlsx";
                    document.body.appendChild(link);
                    link.click();
                },
                error: function (xhr, textStatus, errorThrown) {
                    console.error("Error downloading file:", errorThrown);
                },
            });
        }
    });
});

$("#archiveRotatingShiftAssign").click(function (e) {
    e.preventDefault();
    ids = [];
    ids.push($("#selectedRShifts").attr("data-ids"));
    ids = JSON.parse($("#selectedRShifts").attr("data-ids"));
    if (ids.length === 0) {
        Swal.fire({
            text: i18nMessages.noRowsSelected,
            icon: "warning",
            confirmButtonText: i18nMessages.close,
        });
    } else {
        Swal.fire({
            text: i18nMessages.confirmBulkArchive,
            icon: "info",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#6c757d",
            confirmButtonText: i18nMessages.confirm,
            cancelButtonText: i18nMessages.cancel,
        }).then(function (result) {
            if (result.isConfirmed) {
                ids = [];
                ids.push($("#selectedRShifts").attr("data-ids"));
                ids = JSON.parse($("#selectedRShifts").attr("data-ids"));
                $.ajax({
                    type: "POST",
                    url: "/rotating-shift-assign-bulk-archive/?is_active=False",
                    data: {
                        csrfmiddlewaretoken: getCookie("csrftoken"),
                        ids: JSON.stringify(ids),
                    },
                    success: function (response, textStatus, jqXHR) {
                        if (jqXHR.status === 200) {
                            location.reload(); // Reload the current page
                        } else {
                            // console.log("Unexpected HTTP status:", jqXHR.status);
                        }
                    },
                });
            }
        });
    }
});

$("#unArchiveRotatingShiftAssign").click(function (e) {
    e.preventDefault();
    ids = [];
    ids.push($("#selectedRShifts").attr("data-ids"));
    ids = JSON.parse($("#selectedRShifts").attr("data-ids"));
    if (ids.length === 0) {
        Swal.fire({
            text: i18nMessages.noRowsSelected,
            icon: "warning",
            confirmButtonText: i18nMessages.close,
        });
    } else {
        Swal.fire({
            text: i18nMessages.confirmBulkUnArchive,
            icon: "info",
            showCancelButton: true,
            confirmButtonColor: "#008000",
            cancelButtonColor: "#6c757d",
            confirmButtonText: i18nMessages.confirm,
            cancelButtonText: i18nMessages.cancel,
        }).then(function (result) {
            if (result.isConfirmed) {
                ids = [];
                ids.push($("#selectedRShifts").attr("data-ids"));
                ids = JSON.parse($("#selectedRShifts").attr("data-ids"));
                $.ajax({
                    type: "POST",
                    url: "/rotating-shift-assign-bulk-archive/?is_active=True",
                    data: {
                        csrfmiddlewaretoken: getCookie("csrftoken"),
                        ids: JSON.stringify(ids),
                    },
                    success: function (response, textStatus, jqXHR) {
                        if (jqXHR.status === 200) {
                            location.reload(); // Reload the current page
                        } else {
                            // console.log("Unexpected HTTP status:", jqXHR.status);
                        }
                    },
                });
            }
        });
    }
});

$("#deleteRotatingShiftAssign").click(function (e) {
    e.preventDefault();
    ids = [];
    ids.push($("#selectedRShifts").attr("data-ids"));
    ids = JSON.parse($("#selectedRShifts").attr("data-ids"));
    if (ids.length === 0) {
        Swal.fire({
            text: i18nMessages.noRowsSelected,
            icon: "warning",
            confirmButtonText: i18nMessages.close,
        });
    } else {
        Swal.fire({
            text: i18nMessages.confirmBulkDelete,
            icon: "error",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#6c757d",
            confirmButtonText: i18nMessages.confirm,
            cancelButtonText: i18nMessages.cancel,
        }).then(function (result) {
            if (result.isConfirmed) {
                ids = [];
                ids.push($("#selectedRShifts").attr("data-ids"));
                ids = JSON.parse($("#selectedRShifts").attr("data-ids"));
                $.ajax({
                    type: "POST",
                    url: "/rotating-shift-assign-bulk-delete/",
                    data: {
                        csrfmiddlewaretoken: getCookie("csrftoken"),
                        ids: JSON.stringify(ids),
                    },
                    success: function (response, textStatus, jqXHR) {
                        if (jqXHR.status === 200) {
                            location.reload(); // Reload the current page
                        } else {
                            // console.log("Unexpected HTTP status:", jqXHR.status);
                        }
                    },
                });
            }
        });
    }
});

$(".all-rwork-from").change(function (e) {
    var is_checked = $(this).is(":checked");
    var closest = $(this)
        .closest(".oh-sticky-table__thead")
        .siblings(".oh-sticky-table__tbody");
    if (is_checked) {
        $(closest)
            .children()
            .find(".all-rwork-from-row")
            .prop("checked", true)
            .closest(".oh-sticky-table__tr")
            .addClass("highlight-selected");
    } else {
        $(closest)
            .children()
            .find(".all-rwork-from-row")
            .prop("checked", false)
            .closest(".oh-sticky-table__tr")
            .removeClass("highlight-selected");
    }
});

function tickRWorkFromCheckboxes() {
    var ids = JSON.parse($("#selectedRWorkFroms").attr("data-ids") || "[]");
    uniqueIds = makeWorkFromListUnique(ids);
    toggleHighlight(uniqueIds);
    click = $("#selectedRWorkFroms").attr("data-clicked");
    if (click === "1") {
        $(".all-rwork-from").prop("checked", true);
    }
    uniqueIds.forEach(function (id) {
        $("#" + id).prop("checked", true);
    });
    var selectedCount = uniqueIds.length;
    if (selectedCount > 0) {
        $("#exportRWorkFroms").css("display", "inline-flex");
        $("#unselectAllRWorkFroms").css("display", "inline-flex");
        $("#selectedShowRWorkFroms").css("display", "inline-flex");
        $("#selectedShowRWorkFroms").text(selectedCount + " -" + i18nMessages.selected);
    } else {
        $("#selectedShowRWorkFroms").css("display", "none");
        $("#exportRWorkFroms").css("display", "none");
        $("#unselectAllRWorkFroms").css("display", "none");
    }
}

$("#exportRWorkFroms").click(function (e) {
    var currentDate = new Date().toISOString().slice(0, 10);
    ids = [];
    ids = JSON.parse($("#selectedRWorkFroms").attr("data-ids"));
    Swal.fire({
        text: i18nMessages.downloadExcel,
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#008000",
        cancelButtonColor: "#6c757d",
        confirmButtonText: i18nMessages.confirm,
        cancelButtonText: i18nMessages.cancel,

    }).then(function (result) {
        if (result.isConfirmed) {
            $.ajax({
                type: "GET",
                url: "/rotating-work-from-assign-export",
                data: {
                    ids: JSON.stringify(ids),
                },
                dataType: "binary",
                xhrFields: {
                    responseType: "blob",
                },
                success: function (response) {
                    const file = new Blob([response], {
                        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    });
                    const url = URL.createObjectURL(file);
                    const link = document.createElement("a");
                    link.href = url;
                    link.download = "Rotating_work_from_assign" + currentDate + ".xlsx";
                    document.body.appendChild(link);
                    link.click();
                },
                error: function (xhr, textStatus, errorThrown) {
                    console.error("Error downloading file:", errorThrown);
                },
            });
        }
    });
});

$("#archiveRotatingWorkFromAssign").click(function (e) {
    var ids = JSON.parse($("#selectedRWorkFroms").attr("data-ids"));
    if (ids.length === 0) {
        Swal.fire({
            text: i18nMessages.noRowsSelected,
            icon: "warning",
            confirmButtonText: i18nMessages.close,
        });
    } else {
        Swal.fire({
            text: i18nMessages.confirmBulkArchive,
            icon: "info",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#6c757d",
            confirmButtonText: i18nMessages.confirm,
            cancelButtonText: i18nMessages.cancel,
        }).then(function (result) {
            if (result.isConfirmed) {
                var idsString = JSON.stringify(ids);
                var hxSpan = $("#archiveRotatingWorkFromAssignSpan");
                hxSpan.attr("hx-vals", JSON.stringify({ ids: idsString, is_active: false }));
                hxSpan.click();
            }
        });
    }
});

$("#unArchiveRotatingWorkFromAssign").click(function (e) {
    e.preventDefault();
    var ids = JSON.parse($("#selectedRWorkFroms").attr("data-ids"));
    if (ids.length === 0) {
        Swal.fire({
            text: i18nMessages.noRowsSelected,
            icon: "warning",
            confirmButtonText: i18nMessages.close,
        });
    } else {
        Swal.fire({
            text: i18nMessages.confirmBulkUnArchive,
            icon: "info",
            showCancelButton: true,
            confirmButtonColor: "#008000",
            cancelButtonColor: "#6c757d",
            confirmButtonText: i18nMessages.confirm,
            cancelButtonText: i18nMessages.cancel,
        }).then(function (result) {
            if (result.isConfirmed) {
                var idsString = JSON.stringify(ids);
                var hxSpan = $("#archiveRotatingWorkFromAssignSpan");
                hxSpan.attr("hx-vals", JSON.stringify({ ids: idsString, is_active: true }));
                hxSpan.click();
            }
        });
    }
});


$("#deleteRotatingWorkFromAssign").click(function (e) {
    e.preventDefault();

    ids = [];
    ids.push($("#selectedRWorkFroms").attr("data-ids"));
    ids = JSON.parse($("#selectedRWorkFroms").attr("data-ids"));
    if (ids.length === 0) {
        Swal.fire({
            text: i18nMessages.noRowsSelected,
            icon: "warning",
            confirmButtonText: i18nMessages.close,
        });
    } else {
        Swal.fire({
            text: i18nMessages.confirmBulkDelete,
            icon: "error",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#6c757d",
            confirmButtonText: i18nMessages.confirm,
            cancelButtonText: i18nMessages.cancel,
        }).then(function (result) {
            if (result.isConfirmed) {
                ids = [];
                ids.push($("#selectedRWorkFroms").attr("data-ids"));
                ids = JSON.parse($("#selectedRWorkFroms").attr("data-ids"));
                $.ajax({
                    type: "POST",
                    url: "/rotating-work-from-assign-bulk-delete/",
                    data: {
                        csrfmiddlewaretoken: getCookie("csrftoken"),
                        ids: JSON.stringify(ids),
                    },
                    success: function (response, textStatus, jqXHR) {
                        if (jqXHR.status === 200) {
                            location.reload(); // Reload the current page
                        } else {
                            // console.log("Unexpected HTTP status:", jqXHR.status);
                        }
                    },
                });
            }
        });
    }
});

$(".all-shift-requests").change(function (e) {
    var is_checked = $(this).is(":checked");
    var closest = $(this)
        .closest(".oh-sticky-table__thead")
        .siblings(".oh-sticky-table__tbody");
    if (is_checked) {
        $(closest)
            .children()
            .find(".all-shift-requests-row")
            .prop("checked", true)
            .closest(".oh-sticky-table__tr")
            .addClass("highlight-selected");
    } else {
        $(closest)
            .children()
            .find(".all-shift-requests-row")
            .prop("checked", false)
            .closest(".oh-sticky-table__tr")
            .removeClass("highlight-selected");
    }
});

function tickShiftCheckboxes() {
    var ids = JSON.parse($("#selectedShifts").attr("data-ids") || "[]");
    uniqueIds = makeShiftListUnique(ids);
    toggleHighlight(uniqueIds);
    click = $("#selectedShifts").attr("data-clicked");
    if (click === "1") {
        $(".all-shift-requests").prop("checked", true);
    }
    uniqueIds.forEach(function (id) {
        $("#" + id).prop("checked", true);
    });
    var selectedCount = uniqueIds.length;
    if (selectedCount > 0) {
        $("#exportShifts").css("display", "inline-flex");
        $("#unselectAllShifts").css("display", "inline-flex");
        $("#selectedShowShifts").css("display", "inline-flex");
        $("#selectedShowShifts").text(selectedCount + " -" + i18nMessages.selected);
    } else {
        $("#selectedShowShifts").css("display", "none");
        $("#exportShifts").css("display", "none");
        $("#unselectAllShifts").css("display", "none");
    }
}

function exportShiftRequests() {
    var currentDate = new Date().toISOString().slice(0, 10);
    ids = [];
    ids = JSON.parse($("#selectedShifts").attr("data-ids"));
    Swal.fire({
        text: i18nMessages.downloadExcel,
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#008000",
        cancelButtonColor: "#6c757d",
        confirmButtonText: i18nMessages.confirm,
        cancelButtonText: i18nMessages.cancel,
    }).then(function (result) {
        if (result.isConfirmed) {
            $.ajax({
                type: "GET",
                url: "/shift-request-info-export",
                data: {
                    ids: JSON.stringify(ids),
                },
                dataType: "binary",
                xhrFields: {
                    responseType: "blob",
                },
                success: function (response) {
                    const file = new Blob([response], {
                        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    });
                    const url = URL.createObjectURL(file);
                    const link = document.createElement("a");
                    link.href = url;
                    link.download = "Shift_requests" + currentDate + ".xlsx";
                    document.body.appendChild(link);
                    link.click();
                },
                error: function (xhr, textStatus, errorThrown) {
                    console.error("Error downloading file:", errorThrown);
                },
            });
        }
    });
}

$("#approveShiftRequest").click(function (e) {
    e.preventDefault();
    ids = [];
    ids.push($("#selectedShifts").attr("data-ids"));
    ids = JSON.parse($("#selectedShifts").attr("data-ids"));
    if (ids.length === 0) {
        Swal.fire({
            text: i18nMessages.noRowsSelected,
            icon: "warning",
            confirmButtonText: i18nMessages.close,
        });
    } else {
        // Use SweetAlert for the confirmation dialog
        Swal.fire({
            text: i18nMessages.confirmBulkApprove,
            icon: "success",
            showCancelButton: true,
            confirmButtonColor: "#008000",
            cancelButtonColor: "#6c757d",
            confirmButtonText: i18nMessages.confirm,
            cancelButtonText: i18nMessages.cancel,
        }).then(function (result) {
            if (result.isConfirmed) {
                ids = [];
                ids.push($("#selectedShifts").attr("data-ids"));
                ids = JSON.parse($("#selectedShifts").attr("data-ids"));
                $.ajax({
                    type: "POST",
                    url: "/shift-request-bulk-approve/",
                    data: {
                        csrfmiddlewaretoken: getCookie("csrftoken"),
                        ids: JSON.stringify(ids),
                    },
                    success: function (response, textStatus, jqXHR) {
                        if (jqXHR.status === 200) {
                            location.reload(); // Reload the current page
                        } else {
                            // console.log("Unexpected HTTP status:", jqXHR.status);
                        }
                    },
                });
            }
        });
    }
});

$("#cancelShiftRequest").click(function (e) {
    e.preventDefault();
    ids = [];
    ids.push($("#selectedShifts").attr("data-ids"));
    ids = JSON.parse($("#selectedShifts").attr("data-ids"));
    if (ids.length === 0) {
        Swal.fire({
            text: i18nMessages.noRowsSelected,
            icon: "warning",
            confirmButtonText: i18nMessages.close,
        });
    } else {
        Swal.fire({
            text: i18nMessages.confirmBulkReject,
            icon: "info",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#6c757d",
            confirmButtonText: i18nMessages.confirm,
            cancelButtonText: i18nMessages.cancel,
        }).then(function (result) {
            if (result.isConfirmed) {
                ids = [];
                ids.push($("#selectedShifts").attr("data-ids"));
                ids = JSON.parse($("#selectedShifts").attr("data-ids"));
                $.ajax({
                    type: "POST",
                    url: "/shift-request-bulk-cancel/",
                    data: {
                        csrfmiddlewaretoken: getCookie("csrftoken"),
                        ids: JSON.stringify(ids),
                    },
                    success: function (response, textStatus, jqXHR) {
                        if (jqXHR.status === 200) {
                            location.reload(); // Reload the current page
                        } else {
                            // console.log("Unexpected HTTP status:", jqXHR.status);
                        }
                    },
                });
            }
        });
    }
});

$("#deleteShiftRequest").click(function (e) {
    e.preventDefault();
    ids = [];
    ids.push($("#selectedShifts").attr("data-ids"));
    ids = JSON.parse($("#selectedShifts").attr("data-ids"));
    if (ids.length === 0) {
        Swal.fire({
            text: i18nMessages.noRowsSelected,
            icon: "warning",
            confirmButtonText: i18nMessages.close,
        });
    } else {
        Swal.fire({
            text: i18nMessages.confirmBulkDelete,
            icon: "error",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#6c757d",
            confirmButtonText: i18nMessages.confirm,
            cancelButtonText: i18nMessages.cancel,
        }).then(function (result) {
            if (result.isConfirmed) {
                ids = [];
                ids.push($("#selectedShifts").attr("data-ids"));
                ids = JSON.parse($("#selectedShifts").attr("data-ids"));
                $.ajax({
                    type: "POST",
                    url: "/shift-request-bulk-delete/",
                    data: {
                        csrfmiddlewaretoken: getCookie("csrftoken"),
                        ids: JSON.stringify(ids),
                    },
                    success: function (response, textStatus, jqXHR) {
                        if (jqXHR.status === 200) {
                            location.reload(); // Reload the current page
                        } else {
                            // console.log("Unexpected HTTP status:", jqXHR.status);
                        }
                    },
                });
            }
        });
    }
});

$(".all-work-from-requests").change(function (e) {
    var is_checked = $(this).is(":checked");
    var closest = $(this)
        .closest(".oh-sticky-table__thead")
        .siblings(".oh-sticky-table__tbody");
    if (is_checked) {
        $(closest)
            .children()
            .find(".all-work-from-requests-row")
            .prop("checked", true)
            .closest(".oh-sticky-table__tr")
            .addClass("highlight-selected");
    } else {
        $(closest)
            .children()
            .find(".all-work-from-requests-row")
            .prop("checked", false)
            .closest(".oh-sticky-table__tr")
            .removeClass("highlight-selected");
    }
});

function tickWorkFromCheckboxes() {
    var ids = JSON.parse($("#selectedWorkFroms").attr("data-ids") || "[]");
    uniqueIds = makeWorkFromListUnique(ids);
    toggleHighlight(uniqueIds);
    click = $("#selectedWorkFroms").attr("data-clicked");
    if (click === "1") {
        $(".all-work-from-requests").prop("checked", true);
    }
    uniqueIds.forEach(function (id) {
        $("#" + id).prop("checked", true);
    });
    var selectedCount = uniqueIds.length;
    if (selectedCount > 0) {
        $("#exportWorkFroms").css("display", "inline-flex");
        $("#unselectAllWorkFroms").css("display", "inline-flex");
        $("#selectedShowWorkFroms").css("display", "inline-flex");
        $("#selectedShowWorkFroms").text(selectedCount + " -" + i18nMessages.selected);
    } else {
        $("#selectedShowWorkFroms").css("display", "none");
        $("#exportWorkFroms").css("display", "none");
        $("#unselectAllWorkFroms").css("display", "none");
    }
}

function exportWorkFromRequets() {
    var currentDate = new Date().toISOString().slice(0, 10);
    ids = [];
    ids = JSON.parse($("#selectedWorkFroms").attr("data-ids"));
    Swal.fire({
        text: i18nMessages.downloadExcel,
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#008000",
        cancelButtonColor: "#6c757d",
        confirmButtonText: i18nMessages.confirm,
        cancelButtonText: i18nMessages.cancel,
    }).then(function (result) {
        if (result.isConfirmed) {
            $.ajax({
                type: "GET",
                url: "/work-from-request-info-export",
                data: {
                    ids: JSON.stringify(ids),
                },
                dataType: "binary",
                xhrFields: {
                    responseType: "blob",
                },
                success: function (response) {
                    const file = new Blob([response], {
                        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    });
                    const url = URL.createObjectURL(file);
                    const link = document.createElement("a");
                    link.href = url;
                    link.download = "Work_from_requests" + currentDate + ".xlsx";
                    document.body.appendChild(link);
                    link.click();
                },
                error: function (xhr, textStatus, errorThrown) {
                    console.error("Error downloading file:", errorThrown);
                },
            });
        }
    });
}

$("#approveWorkFromRequest").click(function (e) {
    e.preventDefault();
    ids = [];
    ids.push($("#selectedWorkFroms").attr("data-ids"));
    ids = JSON.parse($("#selectedWorkFroms").attr("data-ids"));
    if (ids.length === 0) {
        Swal.fire({
            text: i18nMessages.noRowsSelected,
            icon: "warning",
            confirmButtonText: i18nMessages.close,
        });
    } else {
        Swal.fire({
            text: i18nMessages.confirmBulkApprove,
            icon: "success",
            showCancelButton: true,
            confirmButtonColor: "#008000",
            cancelButtonColor: "#6c757d",
            confirmButtonText: i18nMessages.confirm,
            cancelButtonText: i18nMessages.cancel,
        }).then(function (result) {
            if (result.isConfirmed) {
                e.preventDefault();
                ids = [];
                ids.push($("#selectedWorkFroms").attr("data-ids"));
                ids = JSON.parse($("#selectedWorkFroms").attr("data-ids"));
                $.ajax({
                    type: "POST",
                    url: "/work-from-request-bulk-approve/",
                    data: {
                        csrfmiddlewaretoken: getCookie("csrftoken"),
                        ids: JSON.stringify(ids),
                    },
                    success: function (response, textStatus, jqXHR) {
                        if (jqXHR.status === 200) {
                            location.reload(); // Reload the current page
                        } else {
                            // console.log("Unexpected HTTP status:", jqXHR.status);
                        }
                    },
                });
            }
        });
    }
});

$("#cancelWorkFromRequest").click(function (e) {
    e.preventDefault();
    ids = [];
    ids.push($("#selectedWorkFroms").attr("data-ids"));
    ids = JSON.parse($("#selectedWorkFroms").attr("data-ids"));
    if (ids.length === 0) {
        Swal.fire({
            text: i18nMessages.noRowsSelected,
            icon: "warning",
            confirmButtonText: i18nMessages.close,
        });
    } else {
        Swal.fire({
            text: i18nMessages.confirmBulkReject,
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#6c757d",
            confirmButtonText: i18nMessages.confirm,
            cancelButtonText: i18nMessages.cancel,
        }).then(function (result) {
            if (result.isConfirmed) {
                ids = [];
                ids.push($("#selectedWorkFroms").attr("data-ids"));
                ids = JSON.parse($("#selectedWorkFroms").attr("data-ids"));
                $.ajax({
                    type: "POST",
                    url: "/work-from-request-bulk-cancel/",
                    data: {
                        csrfmiddlewaretoken: getCookie("csrftoken"),
                        ids: JSON.stringify(ids),
                    },
                    success: function (response, textStatus, jqXHR) {
                        if (jqXHR.status === 200) {
                            location.reload(); // Reload the current page
                        } else {
                            // console.log("Unexpected HTTP status:", jqXHR.status);
                        }
                    },
                });
            }
        });
    }
});

$("#deleteWorkFromRequest").click(function (e) {
    e.preventDefault();
    ids = [];
    ids.push($("#selectedWorkFroms").attr("data-ids"));
    ids = JSON.parse($("#selectedWorkFroms").attr("data-ids"));
    if (ids.length === 0) {
        Swal.fire({
            text: i18nMessages.noRowsSelected,
            icon: "warning",
            confirmButtonText: i18nMessages.close,
        });
    } else {
        Swal.fire({
            text: i18nMessages.confirmBulkDelete,
            icon: "error",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#6c757d",
            confirmButtonText: i18nMessages.confirm,
            cancelButtonText: i18nMessages.cancel,
        }).then(function (result) {
            if (result.isConfirmed) {
                e.preventDefault();
                ids = [];
                ids.push($("#selectedWorkFroms").attr("data-ids"));
                ids = JSON.parse($("#selectedWorkFroms").attr("data-ids"));
                $.ajax({
                    type: "POST",
                    url: "/work-from-request-bulk-delete/",
                    data: {
                        csrfmiddlewaretoken: getCookie("csrftoken"),
                        ids: JSON.stringify(ids),
                    },
                    success: function (response, textStatus, jqXHR) {
                        if (jqXHR.status === 200) {
                            location.reload(); // Reload the current page
                        } else {
                            // console.log("Unexpected HTTP status:", jqXHR.status);
                        }
                    },
                });
            }
        });
    }
});
