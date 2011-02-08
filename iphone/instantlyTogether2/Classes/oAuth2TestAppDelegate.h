//
//  oAuth2TestAppDelegate.h
//  oAuth2Test
//
//  Created by dominic dimarco on 5/22/10.
//  Copyright 214Apps 2010. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "oAuth2TestViewController.h"
@class oAuth2TestViewController;

@interface oAuth2TestAppDelegate : NSObject <UIApplicationDelegate> {
    UIWindow *window;
    oAuth2TestViewController *viewController;
	UINavigationController *navController;
}

@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, retain) IBOutlet oAuth2TestViewController *viewController;
@property (nonatomic, retain) UINavigationController *navController;

@end

