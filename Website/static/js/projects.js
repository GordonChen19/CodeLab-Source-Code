function deleteRoom(roomId) {
    if (confirm("Are you sure you want to delete this room?")) {
        fetch('/projects', {
            method: 'DELETE',
            body: JSON.stringify({ roomId:roomId })
        }).then((_res) => {
            window.location.href = "/projects";
        });
    }
}
