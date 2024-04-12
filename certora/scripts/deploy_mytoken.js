// scripts/deploy_mytoken.js

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);

    const MyToken = await ethers.getContractFactory("MyToken");
    const myToken = await MyToken.deploy("MyToken", "MTK", 18, 1000000);

    console.log("MyToken deployed to:", myToken.address);
}

main().then(() => process.exit(0)).catch((error) => {
    console.error(error);
    process.exit(1);
});
