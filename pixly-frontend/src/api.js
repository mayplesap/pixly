import axios from "axios";

const BASE_URL = "http://localhost:5000/";

/** API Class.
 *
 * Static class tying together methods used to get/send to to the API.
 * There shouldn't be any frontend-specific stuff here, and there shouldn't
 * be any API-aware stuff elsewhere in the frontend.
 *
 */

class PixlyApi {

  static async request(endpoint, data = {}, method = "get") {
    console.debug("API Call:", data, method);

    const url = `${BASE_URL}${endpoint}`;
    // const headers = { Authorization: `Bearer ${JoblyApi.token}` };
    // const headers = { 'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*" };
    const headers = { 'Content-Type': 'application/json, multipart/form-data, application/x-www-form-urlencoded', 
                      "Accept": "application/json" };
    const params = (method === "get")
        ? data
        : {};
    console.log("DATA", data)
    try {
      let res = await axios({ url, method, data, params, headers }); // removed headers
      console.log("RESPONSE", res);
      return res;
    } catch (err) {
      console.error("API Error:", err.response);
      let message = err.response.data.error.message;
      throw Array.isArray(message) ? message : [message];
    }
  }

  // Individual API routes

  /** Upload image. */

  static async uploadImage(data) {
    let res = await this.request('', data, "post");
    return res;
  }

  /** Image Border */

  static async borderImage() {
    let res = await this.request("api/images");
    return res;
  }

  /** Black and White Image */

  static async blackWhiteImage(link) {
    console.log("API BWIMAGE LINK", link)
    let res = await this.request("image", link, "post");
    return res;

  }
}

export default PixlyApi;
