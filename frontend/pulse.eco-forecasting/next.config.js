const dotenv = require('dotenv');

dotenv.config();

module.exports = {
	reactStrictMode: true,
	env: {
		USERNAME: process.env.USERNAME,
		PASSWORD: process.env.PASSWORD,
	},
};
