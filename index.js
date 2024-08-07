import puppeteerExtra from 'puppeteer-extra';
import stealth from 'puppeteer-extra-plugin-stealth';
import fs from 'fs';

puppeteerExtra.use(stealth());

const connectBrowser = async () => {
    const browser = await puppeteerExtra.launch({
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', //Add your browser's executable path here
    });
    const page = await browser.newPage();
    page.setDefaultNavigationTimeout(2 * 60 * 1000);
    return { browser, page };
};

const run = async () => {
    let browser;
    const products = [];

    try {
        const { browser: initialBrowser, page } = await connectBrowser();
        browser = initialBrowser;
        await page.setUserAgent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        );
        await page.goto('https://www.amazon.fr/gp/bestsellers'); //Add your amazon bestseller's list link here
        await page.waitForSelector('li.a-carousel-card', { timeout: 30000 });
        function sleep(ms) {
            return new Promise(resolve =>
                setTimeout(resolve, ms)
            );
        }
        await sleep(10000);
        const initialProducts = await page.evaluate(async () => {
            const items = document.querySelectorAll('li.a-carousel-card');
            return Array.from(items).map(item => {
                const titleElement = item.querySelector('.p13n-sc-truncate-desktop-type2');
                const priceElement = item.querySelector('._cDEzb_p13n-sc-price_3mJ9Z');
                const productURLElement = item.querySelector('a.a-link-normal[href*="/dp/"]');
                const ratingElement = item.querySelector('.a-icon-alt');
                const reviewsCountElement = item.querySelector('.a-size-small');

                const title = titleElement ? titleElement.innerText.trim() : null;
                const price = priceElement ? priceElement.innerText.trim().replace(/\s/g, '').replace(/,/g, '.') : null;
                const url = productURLElement ? productURLElement.href : null;
                const rating = ratingElement ? parseFloat(ratingElement.innerText.split(' sur ')[0].replace(',', '.')) : null;
                const reviewsCount = reviewsCountElement ? parseInt(reviewsCountElement.innerText.replace(/\D/g, ''), 10) : null;

                return { 
                    title,
                    price,
                    url,
                    rating,
                    reviewsCount
                };
            });
        });

        console.log(initialProducts);
        products.push(...initialProducts);

        // Save the products data to a JSON file
        const date = new Date().toISOString().split('T')[0];
        const filename = `products_${date}.json`;

        fs.writeFileSync(filename, JSON.stringify(products, null, 2), 'utf-8');
        console.log(`Products data saved to ${filename}`);

    } catch (e) {
        console.error('Scrape failed', e);
    } finally {
        await browser?.close();
    }
};

await run();