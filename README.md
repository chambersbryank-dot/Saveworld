<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Join the positive movement to save our planet. Practical actions, ocean conservation, sustainable living, and community inspiration.">
    <meta name="keywords" content="save the planet, ocean conservation, environmental action, sustainable living, climate hope, eco friendly, protect our oceans, positive change, green living, earth day">
    <title>Welcome to Save the Planet</title>
    <style>
        :root {
            --primary: #00a8a8;
            --accent: #00cc99;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        
        /* Watermark Ocean Background */
        .hero {
            background: linear-gradient(rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.45)),
                        url('https://images.pexels.com/photos/29142237/pexels-photo-29142237.jpeg') center/cover no-repeat fixed;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: white;
            position: relative;
        }
        
        .hero-content {
            z-index: 2;
            max-width: 800px;
            padding: 2rem;
        }
        
        .hero h1 {
            font-size: 4.5rem;
            margin-bottom: 1rem;
            text-shadow: 0 4px 15px rgba(0,0,0,0.6);
        }
        
        .hero p {
            font-size: 1.6rem;
            margin-bottom: 2rem;
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }
        
        /* Sticky Navigation */
        nav {
            position: sticky;
            top: 0;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 70px;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--primary);
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            list-style: none;
        }
        
        .nav-links a {
            text-decoration: none;
            color: #333;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .nav-links a:hover {
            color: var(--primary);
        }
        
        .btn {
            background: var(--primary);
            color: white;
            padding: 10px 24px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .btn:hover {
            background: var(--accent);
            transform: translateY(-3px);
        }
        
        /* Sections */
        section {
            padding: 5rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h2 {
            text-align: center;
            font-size: 2.8rem;
            margin-bottom: 3rem;
            color: var(--primary);
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            transition: transform 0.3s;
        }
        
        .card:hover {
            transform: translateY(-10px);
        }
        
        footer {
            background: #0a3d3d;
            color: white;
            text-align: center;
            padding: 3rem 2rem;
        }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 3rem; }
            .nav-links { gap: 1rem; font-size: 0.95rem; }
        }
    </style>
</head>
<body>
    <!-- Sticky Nav -->
    <nav>
        <div class="nav-container">
            <div class="logo">🌊 Save The Planet</div>
            <ul class="nav-links">
                <li><a href="#actions">Actions</a></li>
                <li><a href="#learn">Learn</a></li>
                <li><a href="#community">Community</a></li>
                <li><a href="#share">Share</a></li>
            </ul>
            <a href="#join" class="btn">Join the Movement</a>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <h1>Welcome to a Brighter Future</h1>
            <p>Together, we're protecting our beautiful oceans and building a thriving planet for generations to come.</p>
            <a href="#actions" class="btn" style="font-size: 1.3rem; padding: 16px 40px;">Start Making a Positive Impact</a>
        </div>
    </section>

    <!-- Actions Section -->
    <section id="actions">
        <h2>Simple Actions. Big Impact.</h2>
        <div class="grid">
            <div class="card">
                <h3>🌱 Reduce Plastic</h3>
                <p>Switch to reusable bags, bottles, and straws. Every piece of plastic you avoid helps protect marine life.</p>
            </div>
            <div class="card">
                <h3>🌊 Beach & Ocean Cleanups</h3>
                <p>Join or organize local cleanups. Even 30 minutes makes a difference.</p>
            </div>
            <div class="card">
                <h3>🌍 Support Sustainable Choices</h3>
                <p>Choose reef-safe sunscreen, sustainable seafood, and eco-friendly products.</p>
            </div>
        </div>
    </section>

    <!-- Learn Section -->
    <section id="learn" style="background: #f8fffe;">
        <h2>Learn & Discover</h2>
        <div class="grid">
            <div class="card">
                <h3>Ocean Conservation</h3>
                <p>Discover how healthy oceans regulate our climate and support biodiversity.</p>
            </div>
            <div class="card">
                <h3>Sustainable Living Tips</h3>
                <p>Practical daily habits that reduce your environmental footprint.</p>
            </div>
            <div class="card">
                <h3>Success Stories</h3>
                <p>Real examples of communities restoring coral reefs and protecting wildlife.</p>
            </div>
        </div>
    </section>

    <!-- Community & Sharing -->
    <section id="community">
        <h2>Share Knowledge • Build Community</h2>
        <p style="text-align:center; font-size:1.3rem; max-width:700px; margin:0 auto 3rem;">
            The more we share positive solutions and inspiring stories, the faster we create real change.
        </p>
        <div style="text-align:center;">
            <a href="#" class="btn" style="margin:0 1rem; font-size:1.2rem;">Share Your Story</a>
            <a href="#" class="btn" style="margin:0 1rem; font-size:1.2rem; background:#00cc99;">Join Our Community</a>
        </div>
    </section>

    <footer>
        <p>&copy; 2026 Save The Planet • Made with hope for a healthier Earth</p>
        <p style="margin-top:1rem; opacity:0.8;">
            Keywords: Save the Planet • Ocean Conservation • Positive Climate Action • Sustainable Future
        </p>
    </footer>
</body>
</html>
