<template>
  <div class="page-container">
    <div class="top-box">
      <h1 class="heading">Games Library</h1>
      <hr />
      <br />
      <b-alert variant="success" v-if="showMessage" :show="showMessage">
        {{ message }}
      </b-alert>

      <button
        type="button"
        class="btn btn-success btn-sm"
        @click="showAddGameModal"
      >
        Add Game
      </button>
      <br /><br />
      <table class="table table-hover">
        <thead>
          <tr>
            <!-- table header cells -->
            <th scope="col">Title</th>
            <th scope="col">Genre</th>
            <th scope="col">Played ?</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="game in games" :key="game.id">
            <!-- table data cells -->
            <td>{{ game.title }}</td>
            <td>{{ game.genre }}</td>
            <td>
              <span v-if="game.played">Yes</span>
              <span v-else>No</span>
            </td>
            <td>
              <div class="btn-group" role="group">
                <!-- 2 Handle update button click -->
                <button
                  type="button"
                  class="btn btn-info btn-sm"
                  v-b-modal.game-update-modal
                  @click="editGame(game)"
                >
                  Update
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="deleteGame(game)"
                >
                  Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <Footer class="text-center" style="border-radius: 10px"
        >Copyright &copy;. All Rights Reserved 2021.</Footer
      >
      <!-- First Model -->
      <b-modal ref="addGameModal" title="Add Game" hide-backdrop hide-footer>
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-group
            id="form-tite-group"
            label="title"
            label-for="form-tite-input"
          >
            <b-form-input
              id="form-tite-input"
              type="text"
              v-model="addGameForm.title"
              required
              placeholder="Enter a Game"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-genre-group"
            label="Genre"
            label-for="form-genre-input"
          >
            <b-form-input
              id="form-genre-input"
              type="text"
              v-model="addGameForm.genre"
              required
              placeholder="Enter a Genre"
            >
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-played-group">
            <b-form-checkbox-group
              v-model="addGameForm.played"
              id="form-checks"
            >
              <b-form-checkbox value="true">Played?</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>

          <b-button type="submit" variant="outline-info">Submit</b-button>
          <b-button type="reset" variant="outline-danger">Reset</b-button>
        </b-form>
      </b-modal>

      <!-- Start of Modal 2 -->
      <b-modal
        ref="editGameModal"
        id="game-update-modal"
        title="Update"
        hide-backdrop
        hide-footer
      >
        <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
          <b-form-group
            id="form-title-edit-group"
            label="Title:"
            label-for="form-title-edit-input"
          >
            <b-form-input
              id="form-title-edit-input"
              type="text"
              v-model="editForm.title"
              required
              placeholder="Enter title"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-genre-edit-group"
            label="Genre:"
            label-for="form-genre-edit-input"
          >
            <b-form-input
              id="form-genre-edit-input"
              type="text"
              v-model="editForm.genre"
              required
              placeholder="Enter genre"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group id="form-played-edit-group">
            <b-form-checkbox-group v-model="editForm.played" id="form-checks">
              <b-form-checkbox value="true">Played?</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>

          <b-button-group>
            <b-button type="submit" variant="outline-info">Update</b-button>
            <b-button type="reset" variant="outline-danger">Cancel</b-button>
          </b-button-group>
        </b-form>
      </b-modal>
      <!-- end of modal 2 -->
    </div>
  </div>
</template>

<script>
export default {
  name: "GamesLibrary",
};
</script>

<style scoped>
/* Full-page container */
.page-container {
  background-color: #f8f9fa; /* Light background */
  height: 100vh; /* Full viewport height */
  display: flex;
  justify-content: center;
  align-items: flex-start; /* Align to the top */
  padding-top: 20px; /* Add spacing at the top */
}

/* Box styling */
.top-box {
  width: 75%; /* Box width */
  padding: 40px; /* Padding inside the box */
  background-color: #ffffff; /* White background */
  border: 2px solid #007bff; /* Blue border */
  border-radius: 10px; /* Rounded corners */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow */
  text-align: center; /* Center text inside the box */
  margin-top: 20px; /* Position the box from the top */
}

/* Heading styling */
.heading {
  font-size: 2.5rem; /* Large font size */
  color: #007bff; /* Blue text */
  font-weight: bold;
}
</style>

<script>
import axios from "axios";
export default {
  name: "GamesLibrary",
  data() {
    return {
      games: [],
      addGameForm: {
        title: "",
        genre: "",
        played: [],
      },
      message: "", // Moved inside the data function
      showMessage: false, // Add this to track the alert visibility
      editForm: {
        id: "",
        title: "",
        genre: "",
        played: [],
      },
    };
  },
  methods: {
    // Get all games from the API
    showAddGameModal() {
      this.$refs.addGameModal.show();
    },
    getGames() {
      const path = "http://127.0.0.1:5000/games";
      axios
        .get(path)
        .then((res) => {
          this.games = res.data.games;
          this.message = "Games added successfully";
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    // POST A NEW GAME
    addGame(payload) {
      const path = "http://127.0.0.1:5000/games";
      axios
        .post(path, payload)
        .then((res) => {
          this.getGames();
        })
        .catch((error) => {
          console.error(error);
          this.getGames();
        });
    },

    initForm() {
      this.addGameForm.title = "";
      this.addGameForm.genre = "";
      this.addGameForm.played = [];
    },
    onSubmit(e) {
      e.preventDefault();
      this.$refs.addGameModal.hide();
      let played = false;
      if (this.addGameForm.played[0]) {
        played = true;
      }
      const payload = {
        title: this.addGameForm.title,
        genre: this.addGameForm.genre,
        played,
      };
      this.addGame(payload);
      this.initForm();
    },
    onReset() {
      this.$refs.addGameModal.hide();
      this.initForm();
    },
    // MODAL 2
    // a- Handle the form Submit after updating
    onSubmitUpdate(e) {
      e.preventDefault();
      this.$refs.editGameModal.hide();
      let played = false;
      if (this.editForm.played[0]) played = true;
      const payload = {
        title: this.editForm.title,
        genre: this.editForm.genre,
        played,
      };
      this.updateGame(payload, this.editForm.id);
    },

    // b- On reset method to reset items to default values
    onReset(e) {
      e.preventDefault();
      this.$refs.addGameModal.hide();
      this.initForm();
    },

    // 4 Update Alert Message
    // Once the update is effective, we will get a message telling us that Game Updated, and display the list of games after the update
    updateGame(payload, gameID) {
      const path = `http://localhost:5000/games/${gameID}`;
      axios
        .put(path, payload)
        .then(() => {
          this.getGames();
          this.message = "Game updated ⚙️!";
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getGames();
        });
    },

    // Handle Update Button
    editGame(game) {
      this.editForm = game;
    },

    // 5 Handle reset / cancel button click
    onResetUpdate(e) {
      e.preventDefault();
      this.$refs.editGameModal.hide();
      this.initForm();
      this.getGames();
    },

    // Remove Game [ Delete Button ]
    removeGame(gameID) {
      const path = `http://localhost:5000/games/${gameID}`;
      axios
        .delete(path)
        .then(() => {
          this.getGames();
          this.message = "Game Removed 🗑️!";
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getGames();
        });
    },
    // Handle Delete Button
    deleteGame(game) {
      this.removeGame(game.id);
    },
  },
  created() {
    this.getGames();
  },
};
</script>
