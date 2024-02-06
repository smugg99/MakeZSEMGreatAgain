import asyncio
import random
import string
from playwright.async_api import async_playwright

async def generate_random_user_agent():
    browser = random.choice(["Chrome", "Firefox", "Safari", "Edge"])
    os = random.choice(["Windows", "Macintosh", "Linux"])
    version = '.'.join([str(random.randint(0, 99)) for _ in range(3)])

    user_agent = f"Mozilla/5.0 ({os}; {browser}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"
    
    return user_agent

async def generate_random_mac_address():
    mac_address = ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])
    
    return mac_address

async def run_survey_instance():
    async with async_playwright() as p:
        user_agent = await generate_random_user_agent()
        mac_address = await generate_random_mac_address()
        
        user_agent = f"{user_agent} (MacAddr {mac_address})"
        
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()

        await page.goto("https://lgbtplusme.com/ranking/pl/evaluation/A4pVVEe2LfYY8X5R5VHud")
        await page.wait_for_load_state("networkidle")

        questions = await page.evaluate('''
            Array.from(document.querySelectorAll('fieldset')).map(fieldset => {
                const question = fieldset.querySelector('legend').textContent.trim();
                const options = Array.from(fieldset.querySelectorAll('input[type="radio"]')).map(input => {
                    return {
                        label: input.nextElementSibling.textContent.trim(),
                        value: input.value
                    };
                });
                return { question, options };
            });
        ''')

        answers = [0,2,0,0,0,1,1,0,2,2,2,2,2,2,2,0,0,0,0,1,0,0,1,0,1,1]

        for i, answer_index in enumerate(answers):
            await page.click(f'input[name="q{i}"][value="{answer_index}"]', force=True)
            await asyncio.sleep(random.uniform(0.5, 2))

        print("Survey completed.")

        await browser.close()

async def run_multiple_instances(num_instances):
    await asyncio.gather(*[run_survey_instance() for _ in range(num_instances)])

NUM_INSTANCES = 10
asyncio.run(run_multiple_instances(NUM_INSTANCES))