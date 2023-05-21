function deleteRoom(roomID) {
    if (confirm("Are you sure you want to delete this room?")) {
        fetch('/projects', {
            method: 'DELETE',
            body: JSON.stringify({ roomID:roomID })
        }).then((_res) => {
            window.location.href = "/projects";
        });
    }
}
