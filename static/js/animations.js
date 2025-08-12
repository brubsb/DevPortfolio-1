/**
 * Animations JavaScript file for Portfolio
 * Handles advanced animations, particle effects, and interactive elements
 */

(function() {
    'use strict';

    // ======================================
    // INITIALIZATION
    // ======================================

    document.addEventListener('DOMContentLoaded', function() {
        initializeAOS();
        initializeParticleEffects();
        initializeHoverAnimations();
        initializeScrollAnimations();
        initializeInteractiveElements();
    });

    // ======================================
    // AOS (Animate On Scroll) INITIALIZATION
    // ======================================

    function initializeAOS() {
        if (typeof AOS !== 'undefined') {
            AOS.init({
                duration: 800,
                easing: 'ease-in-out',
                once: true,
                offset: 50,
                disable: function() {
                    return window.innerWidth < 768; // Disable on mobile for performance
                }
            });

            // Refresh AOS on dynamic content changes
            window.addEventListener('resize', function() {
                setTimeout(() => {
                    AOS.refresh();
                }, 500);
            });
        }
    }

    // ======================================
    // PARTICLE EFFECTS
    // ======================================

    function initializeParticleEffects() {
        createFloatingParticles();
        createMouseFollowEffect();
    }

    /**
     * Create floating particles in hero section
     */
    function createFloatingParticles() {
        const particleContainer = document.querySelector('.particles');
        if (!particleContainer) return;

        // Create additional animated particles
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'floating-particle';
            particle.style.cssText = `
                position: absolute;
                width: ${Math.random() * 4 + 1}px;
                height: ${Math.random() * 4 + 1}px;
                background: rgba(59, 130, 246, ${Math.random() * 0.5 + 0.2});
                border-radius: 50%;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: floatParticle ${Math.random() * 10 + 10}s linear infinite;
                animation-delay: ${Math.random() * 5}s;
            `;
            particleContainer.appendChild(particle);
        }

        // Add CSS for particle animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes floatParticle {
                0% {
                    transform: translateY(100vh) translateX(0) rotate(0deg);
                    opacity: 0;
                }
                10% {
                    opacity: 1;
                }
                90% {
                    opacity: 1;
                }
                100% {
                    transform: translateY(-100px) translateX(100px) rotate(360deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Mouse follow effect for cursor
     */
    function createMouseFollowEffect() {
        const cursor = document.createElement('div');
        cursor.className = 'custom-cursor';
        cursor.style.cssText = `
            position: fixed;
            width: 20px;
            height: 20px;
            background: rgba(59, 130, 246, 0.3);
            border: 2px solid rgba(59, 130, 246, 0.8);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            transition: transform 0.1s ease;
            transform: translate(-50%, -50%);
        `;
        document.body.appendChild(cursor);

        const cursorDot = document.createElement('div');
        cursorDot.className = 'cursor-dot';
        cursorDot.style.cssText = `
            position: fixed;
            width: 4px;
            height: 4px;
            background: rgba(59, 130, 246, 1);
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
            transition: transform 0.05s ease;
            transform: translate(-50%, -50%);
        `;
        document.body.appendChild(cursorDot);

        // Only show custom cursor on desktop
        if (window.innerWidth > 1024) {
            document.addEventListener('mousemove', function(e) {
                cursor.style.left = e.clientX + 'px';
                cursor.style.top = e.clientY + 'px';
                cursorDot.style.left = e.clientX + 'px';
                cursorDot.style.top = e.clientY + 'px';
            });

            // Cursor interactions
            const interactiveElements = document.querySelectorAll('a, button, .portfolio-card, .skill-item');
            
            interactiveElements.forEach(element => {
                element.addEventListener('mouseenter', function() {
                    cursor.style.transform = 'translate(-50%, -50%) scale(1.5)';
                    cursor.style.background = 'rgba(59, 130, 246, 0.1)';
                });

                element.addEventListener('mouseleave', function() {
                    cursor.style.transform = 'translate(-50%, -50%) scale(1)';
                    cursor.style.background = 'rgba(59, 130, 246, 0.3)';
                });
            });
        } else {
            cursor.style.display = 'none';
            cursorDot.style.display = 'none';
        }
    }

    // ======================================
    // HOVER ANIMATIONS
    // ======================================

    function initializeHoverAnimations() {
        initializeCardHoverEffects();
        initializeButtonHoverEffects();
        initializeImageHoverEffects();
    }

    /**
     * Card hover effects with 3D transform
     */
    function initializeCardHoverEffects() {
        const cards = document.querySelectorAll('.portfolio-card, .skills-category');

        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transition = 'transform 0.3s ease';
                this.style.transform = 'translateY(-10px) rotateX(5deg) rotateY(5deg)';
                this.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.2)';
            });

            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) rotateX(0) rotateY(0)';
                this.style.boxShadow = '';
            });

            // Mousemove for subtle tilt effect
            card.addEventListener('mousemove', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                this.style.transform = `translateY(-10px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            });
        });
    }

    /**
     * Button hover effects with ripple animation
     */
    function initializeButtonHoverEffects() {
        const buttons = document.querySelectorAll('.btn');

        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;

                ripple.style.cssText = `
                    position: absolute;
                    width: ${size}px;
                    height: ${size}px;
                    left: ${x}px;
                    top: ${y}px;
                    background: rgba(255, 255, 255, 0.3);
                    border-radius: 50%;
                    transform: scale(0);
                    animation: ripple 0.6s ease-out;
                    pointer-events: none;
                `;

                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                this.appendChild(ripple);

                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });

        // Add ripple animation CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(2);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Image hover effects with zoom and overlay
     */
    function initializeImageHoverEffects() {
        const images = document.querySelectorAll('.portfolio-image img, .about-image img');

        images.forEach(img => {
            img.addEventListener('mouseenter', function() {
                this.style.transition = 'transform 0.5s ease';
                this.style.transform = 'scale(1.1) rotate(2deg)';
            });

            img.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1) rotate(0deg)';
            });
        });
    }

    // ======================================
    // SCROLL ANIMATIONS
    // ======================================

    function initializeScrollAnimations() {
        createScrollProgressBar();
        initializeParallaxEffect();
        initializeCounterAnimations();
    }

    /**
     * Scroll progress bar
     */
    function createScrollProgressBar() {
        const progressBar = document.createElement('div');
        progressBar.className = 'scroll-progress';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, #3b82f6, #60a5fa);
            z-index: 10001;
            transition: width 0.1s ease;
        `;
        document.body.appendChild(progressBar);

        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset;
            const docHeight = document.body.scrollHeight - window.innerHeight;
            const scrollPercent = (scrollTop / docHeight) * 100;
            progressBar.style.width = scrollPercent + '%';
        });
    }

    /**
     * Parallax scrolling effect
     */
    function initializeParallaxEffect() {
        const parallaxElements = document.querySelectorAll('.hero-bg-image, .floating-tech');

        if (window.innerWidth > 768) { // Only on desktop for performance
            window.addEventListener('scroll', function() {
                const scrolled = window.pageYOffset;
                const rate = scrolled * -0.5;

                parallaxElements.forEach(element => {
                    element.style.transform = `translateY(${rate}px)`;
                });
            });
        }
    }

    /**
     * Counter animations with intersection observer
     */
    function initializeCounterAnimations() {
        const counters = document.querySelectorAll('[data-count]');

        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.hasAnimated) {
                    animateCounter(entry.target);
                    entry.target.hasAnimated = true;
                }
            });
        }, { threshold: 0.7 });

        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }

    /**
     * Animate individual counter
     */
    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-count'));
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 16);
    }

    // ======================================
    // INTERACTIVE ELEMENTS
    // ======================================

    function initializeInteractiveElements() {
        initializeSkillBarAnimations();
        initializeTypewriterEffect();
        initializeFloatingElements();
    }

    /**
     * Enhanced skill bar animations
     */
    function initializeSkillBarAnimations() {
        const skillSection = document.getElementById('skills');
        if (!skillSection) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const skillBars = entry.target.querySelectorAll('.skill-progress');
                    
                    skillBars.forEach((bar, index) => {
                        setTimeout(() => {
                            const progress = bar.getAttribute('data-progress');
                            bar.style.width = progress + '%';
                            
                            // Add pulse effect
                            bar.style.animation = 'skillPulse 0.5s ease-in-out';
                        }, index * 200);
                    });
                    
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        observer.observe(skillSection);

        // Add skill pulse animation CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes skillPulse {
                0%, 100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
                50% { box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Enhanced typewriter effect
     */
    function initializeTypewriterEffect() {
        const typewriterElements = document.querySelectorAll('[data-typewriter]');

        typewriterElements.forEach(element => {
            const text = element.getAttribute('data-typewriter');
            const speed = parseInt(element.getAttribute('data-speed')) || 100;
            
            element.textContent = '';
            let index = 0;

            function typeChar() {
                if (index < text.length) {
                    element.textContent += text.charAt(index);
                    index++;
                    setTimeout(typeChar, speed);
                }
            }

            // Start typing when element is in view
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        setTimeout(typeChar, 500);
                        observer.unobserve(entry.target);
                    }
                });
            });

            observer.observe(element);
        });
    }

    /**
     * Floating elements animation
     */
    function initializeFloatingElements() {
        const floatingElements = document.querySelectorAll('.floating-tech');

        floatingElements.forEach((element, index) => {
            // Random floating animation
            const randomDelay = Math.random() * 2;
            const randomDuration = 3 + Math.random() * 2;
            
            element.style.animation = `floatRandom ${randomDuration}s ease-in-out infinite`;
            element.style.animationDelay = `${randomDelay}s`;
        });

        // Add floating animation CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes floatRandom {
                0%, 100% { 
                    transform: translateY(0px) rotate(0deg); 
                }
                25% { 
                    transform: translateY(-10px) rotate(90deg); 
                }
                50% { 
                    transform: translateY(-20px) rotate(180deg); 
                }
                75% { 
                    transform: translateY(-10px) rotate(270deg); 
                }
            }
        `;
        document.head.appendChild(style);
    }

    // ======================================
    // PERFORMANCE MONITORING
    // ======================================

    /**
     * Monitor animation performance
     */
    function monitorPerformance() {
        let lastTime = performance.now();
        let frameCount = 0;

        function updateFPS() {
            frameCount++;
            const currentTime = performance.now();
            
            if (currentTime - lastTime >= 1000) {
                const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
                
                // Reduce animations if FPS is too low
                if (fps < 30) {
                    document.body.classList.add('reduce-animations');
                }
                
                frameCount = 0;
                lastTime = currentTime;
            }
            
            requestAnimationFrame(updateFPS);
        }

        requestAnimationFrame(updateFPS);
    }

    // Start performance monitoring
    if (window.requestAnimationFrame) {
        monitorPerformance();
    }

    // ======================================
    // UTILITY FUNCTIONS
    // ======================================

    /**
     * Throttle function for performance
     */
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    /**
     * Debounce function for performance
     */
    function debounce(func, wait, immediate) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    }

    // Apply throttling to scroll events
    window.addEventListener('scroll', throttle(function() {
        // Throttled scroll handlers go here
    }, 16)); // ~60fps

})();
