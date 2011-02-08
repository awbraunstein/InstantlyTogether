//
//  oAuth2TestAppDelegate.m
//  oAuth2Test
//
//  Created by dominic dimarco on 5/22/10.
//  Copyright 214Apps 2010. All rights reserved.
//

#import "oAuth2TestAppDelegate.h"
#import "oAuth2TestViewController.h"

@implementation oAuth2TestAppDelegate

@synthesize window;
@synthesize viewController;
@synthesize navController;

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {    
    
	
	UINavigationController* _navController = [[UINavigationController alloc] initWithRootViewController: viewController];
	self.navController = _navController;
	[_navController release];
    // Override point for customization after app launch    
    [window addSubview:navController.view];
    [window makeKeyAndVisible];
	
	return YES;
}


- (void)dealloc {
    [viewController release];
    [window release];
	[navController release];
    [super dealloc];
}


@end
