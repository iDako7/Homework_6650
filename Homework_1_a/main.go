package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// album represents data about a record album.
type album struct {
    ID     string  `json:"id"`
    Title  string  `json:"title"`
    Artist string  `json:"artist"`
    Price  float64 `json:"price"`
}

// albums slice to seed record album data.
// ? what's the meaning of []album
var albums = []album{
    {ID: "1", Title: "Blue Train", Artist: "John Coltrane", Price: 56.99},
    {ID: "2", Title: "Jeru", Artist: "Gerry Mulligan", Price: 17.99},
    {ID: "3", Title: "Sarah Vaughan and Clifford Brown", Artist: "Sarah Vaughan", Price: 39.99},
}

func main() {
	router := gin.Default()
	router.GET("/albums", getAlbums) // in /albums path, call function getAlbums
	router.GET("/albums/:id", getAlbumByID)
	router.POST("/albums", postAlbums) // in /albums path, call function postAlbums

	router.Run("localhost:8080")
}

// getAlbums responds with the list of all albums as JSON.
func getAlbums(c *gin.Context) {
	// use the method to return formatted json
	// meaning of parameters: (1)status code; (2)response body
    c.IndentedJSON(http.StatusOK, albums)
}

// postAlbums adds an album from JSON received in the request body.
// ~ *gin.Context: pointer, we're passing a reference to the Context object, not a copy
func postAlbums(c *gin.Context) {
	var newAlbum album
	
	// Call BindJSON to bind the received JSON to newAlbum.
	// err := Declares and initializes err in one step.
	// &newAlbum -> passes the address (pointer) so BindJSON can modify newAlbum directly
	// nil: means success 
	if err := c.BindJSON(&newAlbum); err != nil {
		return
	}

	// Add the new album to the slice
	albums = append(albums, newAlbum)
	c.IndentedJSON(http.StatusCreated, newAlbum)
}

// getAlbumByID locates the album whose ID value matches the id parameter sent by the client, 
// then returns that album as a response
func getAlbumByID(c *gin.Context) {
	id := c.Param("id")

	// Loop over the list of albums, looking for an album whose ID value matches the parameter.
	// in Go, index is default returned
	for _, a := range albums {
		if a.ID == id {
			c.IndentedJSON(http.StatusOK, a)
			return
		}
	}
	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "album not found"})
}