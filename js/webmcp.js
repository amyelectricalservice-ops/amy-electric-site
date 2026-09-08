/**
 * WebMCP Implementation for AMY Electric
 * Exposes site tools to AI agents via the browser
 * https://webmachinelearning.github.io/webmcp/
 */

(function() {
  'use strict';

  // Feature detection for WebMCP
  if (!navigator.modelContext) {
    console.log('WebMCP not supported in this browser');
    return;
  }

  const ABORT_CONTROLLER = new AbortController();

  // Tool: Get Business Information
  navigator.modelContext.registerTool({
    name: 'get_business_info',
    description: 'Get AMY Electric business information including hours, license, and service area',
    inputSchema: {
      type: 'object',
      properties: {},
      required: []
    },
    execute: async () => {
      const info = {
        name: 'AMY Electric',
        license: 'C-10 #981578',
        phone: '(818) 302-5614',
        email: 'info@amyelectric.com',
        serviceArea: 'Greater Los Angeles',
        hours: {
          monday: '7:00 AM - 6:00 PM',
          tuesday: '7:00 AM - 6:00 PM',
          wednesday: '7:00 AM - 6:00 PM',
          thursday: '7:00 AM - 6:00 PM',
          friday: '7:00 AM - 6:00 PM',
          saturday: '8:00 AM - 4:00 PM',
          sunday: 'Closed'
        }
      };
      return {
        content: [{ type: 'text', text: JSON.stringify(info, null, 2) }]
      };
    }
  });

  // Tool: Get Services List
  navigator.modelContext.registerTool({
    name: 'get_services',
    description: 'List all electrical services offered by AMY Electric',
    inputSchema: {
      type: 'object',
      properties: {
        category: {
          type: 'string',
          enum: ['residential', 'commercial', 'ev', 'panel', 'all'],
          description: 'Filter services by category'
        }
      },
      required: []
    },
    execute: async ({ category = 'all' }) => {
      const services = {
        residential: [
          'Whole Home Rewiring',
          'Electrical Panel Upgrade',
          'Generator Transfer Switch',
          'Smoke Detector Installation',
          'Ceiling Fan Installation'
        ],
        commercial: [
          'Commercial Electrical Services',
          'Office Wiring',
          'Retail Store Electrical'
        ],
        ev: [
          'EV Charger Installation',
          'Level 2 Charger Setup',
          'Commercial EV Charging Stations'
        ],
        panel: [
          'Panel Upgrade 100A to 200A',
          'Panel Upgrade 200A to 400A',
          'Sub-Panel Installation'
        ]
      };

      let result;
      if (category === 'all') {
        result = Object.values(services).flat();
      } else {
        result = services[category] || [];
      }

      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    }
  });

  // Tool: Get Contact Information
  navigator.modelContext.registerTool({
    name: 'get_contact_info',
    description: 'Get contact details for AMY Electric including phone, email, and address',
    inputSchema: {
      type: 'object',
      properties: {},
      required: []
    },
    execute: async () => {
      const contact = {
        phone: '(818) 302-5614',
        phoneLink: 'tel:18183025614',
        email: 'info@amyelectric.com',
        website: 'https://amyelectric.com',
        serviceArea: 'Greater Los Angeles',
        responseTime: 'Same day response'
      };
      return {
        content: [{ type: 'text', text: JSON.stringify(contact, null, 2) }]
      };
    }
  });

  // Tool: Navigate to Page
  navigator.modelContext.registerTool({
    name: 'navigate_to_page',
    description: 'Navigate to a specific page on the AMY Electric website',
    inputSchema: {
      type: 'object',
      properties: {
        page: {
          type: 'string',
          enum: ['home', 'services', 'cities', 'about', 'contact', 'gallery', 'testimonials'],
          description: 'The page to navigate to'
        }
      },
      required: ['page']
    },
    execute: async ({ page }) => {
      const pages = {
        home: '/',
        services: '/#services',
        cities: '/#cities',
        about: '/about.html',
        contact: '/#contact',
        gallery: '/gallery.html',
        testimonials: '/testimonials.html'
      };

      const url = pages[page];
      if (url) {
        window.location.href = url;
        return {
          content: [{ type: 'text', text: `Navigating to ${page} page` }]
        };
      }
      return {
        content: [{ type: 'text', text: `Unknown page: ${page}` }]
      };
    }
  });

  // Tool: Get Service Areas
  navigator.modelContext.registerTool({
    name: 'get_service_areas',
    description: 'Get list of cities and ZIP codes served by AMY Electric',
    inputSchema: {
      type: 'object',
      properties: {
        type: {
          type: 'string',
          enum: ['cities', 'zips', 'all'],
          description: 'Return cities, ZIP codes, or both'
        }
      },
      required: []
    },
    execute: async ({ type = 'all' }) => {
      const cities = [
        'Los Angeles', 'Sherman Oaks', 'Burbank', 'Glendale',
        'Pasadena', 'Santa Monica', 'West Hollywood', 'Beverly Hills',
        'Culver City', 'Encino', 'Studio City', 'North Hollywood',
        'Van Nuys', 'Tarzana', 'Woodland Hills', 'Calabasas'
      ];

      const zips = [
        '90001', '90024', '90025', '90049', '90064', '90066',
        '90210', '90211', '90212', '90230', '90232', '90272',
        '91303', '91306', '91311', '91316', '91324', '91325',
        '91335', '91340', '91343', '91345', '91356', '91367'
      ];

      let result;
      if (type === 'cities') {
        result = { cities };
      } else if (type === 'zips') {
        result = { zipCodes: zips };
      } else {
        result = { cities, zipCodes: zips };
      }

      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    }
  });

  // Tool: Request Estimate
  navigator.modelContext.registerTool({
    name: 'request_estimate',
    description: 'Request a free estimate for electrical services',
    inputSchema: {
      type: 'object',
      properties: {
        name: {
          type: 'string',
          description: 'Customer name'
        },
        phone: {
          type: 'string',
          description: 'Phone number'
        },
        service: {
          type: 'string',
          description: 'Type of electrical service needed'
        }
      },
      required: ['name', 'phone', 'service']
    },
    execute: async ({ name, phone, service }) => {
      // Scroll to contact form and pre-fill
      const contactForm = document.getElementById('contact');
      if (contactForm) {
        contactForm.scrollIntoView({ behavior: 'smooth' });
      }

      // Try to fill form fields
      const nameField = document.querySelector('#name, [name="name"]');
      const phoneField = document.querySelector('#phone, [name="phone"]');
      const serviceField = document.querySelector('#service, [name="service"]');

      if (nameField) nameField.value = name;
      if (phoneField) phoneField.value = phone;
      if (serviceField) serviceField.value = service;

      return {
        content: [{
          type: 'text',
          text: `Estimate request prepared for ${name}. Please complete the form and submit.`
        }]
      };
    }
  });

  // Cleanup function for when tools are no longer needed
  window.unregisterWebMCPTools = () => {
    ABORT_CONTROLLER.abort();
    console.log('WebMCP tools unregistered');
  };

  console.log('WebMCP tools registered for AMY Electric');
})();
