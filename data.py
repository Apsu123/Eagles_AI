

old_files = {
    "src/routes/+page.svelte": """<script>
  import Header from '$lib/components/Header.svelte';
  import TextAreaBlock from '$lib/components/TextAreaBlock.svelte';
  import Footer from '$lib/components/Footer.svelte';
</script>

<div class="min-h-screen flex flex-col items-center justify-between py-8 px-4">
  <Header />

  <section class="flex flex-col sm:flex-row gap-8 w-full max-w-5xl justify-center items-start">
    <TextAreaBlock />
    <TextAreaBlock />
  </section>

  <Footer />
</div>
""",

    "src/lib/components/Header.svelte": """<header class="w-full flex justify-between items-center max-w-5xl mb-8">
  <nav class="flex gap-8 text-gray-600 text-sm"> GJEROIGJEOI
    <a href="#" class="hover:text-black">Link one</a>
    <a href="#" class="hover:text-black">Link two</a>
  </nav>

  <div class="w-16 h-16 bg-gray-200 flex items-center justify-center rounded">
    <img src="/placeholder.svg" alt="Logo" class="w-8 h-8" />
  </div>

  <div class="flex items-center text-gray-400 hover:text-gray-600 cursor-pointer">
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1011 3a7.5 7.5 0 005.65 13.65z"
      />
    </svg>
  </div>
</header>
""",

    "src/lib/components/TextAreaBlock.svelte": """<div class="flex flex-col w-full sm:w-1/2 items-center gap-4">
  <textarea
    class="w-full h-72 border border-gray-400 p-2 rounded resize-none"
    placeholder="Type here..."
  ></textarea>
  <button class="w-full bg-gray-700 text-white py-2 rounded hover:bg-gray-800">
    Button
  </button>
</div>
""",

    "src/lib/components/Footer.svelte": """<footer class="w-full mt-12 text-center text-sm text-gray-600 flex justify-center gap-6">
  <a href="#" class="hover:text-black">Link one</a>
  <a href="#" class="hover:text-black">Link two</a>
  <a href="#" class="hover:text-black">Link three</a>
  <a href="#" class="hover:text-black">Link four</a>
</footer>
"""
}


updated_files = {

    "src/routes/+layout.svelte": """
<script>
  import Header from './components/Header.svelte';
  import Footer from './components/Footer.svelte';
</script>

<Header />
<main class="min-h-screen px-4 py-8">
  <slot />
</main>
<Footer />
""",

    "src/routes/+page.svelte": """
<script>
  import TextAreaCard from './components/TextAreaCard.svelte';
</script>

<div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto">
  <TextAreaCard />
  <TextAreaCard />
</div>
""",

    "src/lib/components/Header.svelte": """
<nav class="flex justify-between items-center p-6 bg-white shadow">
  <div class="flex items-center gap-12">
    <a href="#" class="text-gray-700 hover:text-black">Link one</a>
    <a href="#" class="text-gray-700 hover:text-black">Link two</a>
  </div>
  <div class="w-12 h-12 bg-gray-200 flex items-center justify-center rounded">
    <img src="https://via.placeholder.com/40" alt="Logo" />
  </div>
</nav>
""",

    "src/lib/components/Footer.svelte": """
<footer class="mt-16 py-6 border-t text-center text-sm text-gray-500">
  <div class="space-x-6">
    <a href="#" class="hover:underline">Link one</a>
    <a href="#" class="hover:underline">Link two</a>
    <a href="#" class="hover:underline">Link three</a>
    <a href="#" class="hover:underline">Link four</a>
  </div>
</footer>
""",

    "src/lib/components/TextAreaCard.svelte": """
<div class="flex flex-col gap-4">
  <textarea class="border border-gray-400 w-full h-64 p-2 resize-none rounded" placeholder="Type here..."></textarea>
  <button class="bg-gray-700 text-white py-2 rounded hover:bg-gray-800">Button</button>
</div>
"""
}
