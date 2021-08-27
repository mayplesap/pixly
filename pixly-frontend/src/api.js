import axios from "axios";

const BASE_URL = "http://localhost:5000/";

/** API Class.
 *
 * Static class tying together methods used to get/send to to the API.
 *
 */

class PixlyApi {

  static async request(endpoint, data = {}, method = "get") {
    console.debug("API Call:", data, method);

    const url = `${BASE_URL}${endpoint}`;
    const headers = { 'Content-Type': 'application/json, multipart/form-data, application/x-www-form-urlencoded', 
                      "Accept": "application/json" };
    const params = (method === "get")
        ? data
        : {};
    try {
      let res = await axios({ url, method, data, params, headers }); 
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

  /** Image Border (unused) */

  static async borderImage() {
    let res = await this.request("api/images");
    return res;
  }

  /** Black and White Image */

  static async blackWhiteImage(link) {
    let res = await this.request("image/bw", link, "post");
    return res;

  }
  /** Sepia Image */

  static async sepiaImage(link) {
    let res = await this.request("image/sepia", link, "post");
    return res;

  }
  /** "Alien"/Color Merge Image */

  static async colorMergeImage(link) {
    let res = await this.request("image/merge", link, "post");
    return res;


  }
  /** Pointilize Image */

  static async pointilizeImage(link) {
    let res = await this.request("image/pt", link, "post");
    return res;

  }

  /** Add Border to Image */

  static async addBorder(link) {
    let res = await this.request("image/border", link, "post");
    return res;
  }
}

export default PixlyApi;
